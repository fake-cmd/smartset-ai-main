import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

load_dotenv()

try:
    DATABASE_URL = os.getenv("DATABASE_URL") or st.secrets["DATABASE_URL"]
    MODEL_PATH = os.getenv("MODEL_PATH") or st.secrets["MODEL_PATH"]
except Exception:
    st.error("Missing DATABASE_URL or MODEL_PATH. Add them in Streamlit Cloud secrets or local .env.")
    st.stop()
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="SmartSet AI", layout="wide")
st_autorefresh(interval = 60000, debounce=True, key="smartset_refresh")

st.title("SmartSet AI Dashboard")
st.caption("Smart energy analytics, anomaly detection, forecasting, and recommendations")


energy_query = """
SELECT 
    er.id,
    er.device_id,
    d.device_name,
    d.device_type,
    r.room_name,
    h.id AS household_id,
    h.household_name,
    h.location,
    er.timestamp,
    er.power_consumption,
    er.voltage,
    er.current
FROM energy_readings er
JOIN devices d ON er.device_id = d.id
JOIN rooms r ON d.room_id = r.id
JOIN households h ON r.household_id = h.id
"""

anomaly_query = """
SELECT 
    a.id,
    a.device_id,
    d.device_name,
    d.device_type,
    r.room_name,
    h.id AS household_id,
    h.household_name,
    h.location,
    a.anomaly_score,
    a.anomaly_type,
    a.detected_at
FROM anomalies a
JOIN devices d ON a.device_id = d.id
JOIN rooms r ON d.room_id = r.id
JOIN households h ON r.household_id = h.id
"""

household_query = """
SELECT
    h.household_name,
    h.location,
    SUM(er.power_consumption) AS total_consumption
FROM households h
JOIN rooms r ON r.household_id = h.id
JOIN devices d ON d.room_id = r.id
JOIN energy_readings er ON er.device_id = d.id
GROUP BY h.household_name, h.location
ORDER BY total_consumption DESC
"""


df = pd.read_sql(energy_query, engine)
anomalies = pd.read_sql(anomaly_query, engine)
households = pd.read_sql(household_query, engine)

df["timestamp"] = pd.to_datetime(df["timestamp"])
anomalies["detected_at"] = pd.to_datetime(anomalies["detected_at"])


# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Filters")

household_options = ["All"] + sorted(df["household_name"].unique().tolist())

selected_household = st.sidebar.selectbox(
    "Household",
    household_options
)

device_types = ["All"] + sorted(df["device_type"].unique().tolist())

selected_type = st.sidebar.selectbox(
    "Device Type",
    device_types
)


# -----------------------------
# APPLY FILTERS ONCE
# -----------------------------

filtered_df = df.copy()
filtered_anomalies = anomalies.copy()

if selected_household != "All":
    filtered_df = filtered_df[
        filtered_df["household_name"] == selected_household
    ]

    filtered_anomalies = filtered_anomalies[
        filtered_anomalies["household_name"] == selected_household
    ]

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["device_type"] == selected_type
    ]

    filtered_anomalies = filtered_anomalies[
        filtered_anomalies["device_type"] == selected_type
    ]


# -----------------------------
# KPI CARDS
# -----------------------------

total_consumption = filtered_df["power_consumption"].sum()
average_consumption = filtered_df["power_consumption"].mean()
max_consumption = filtered_df["power_consumption"].max()
reading_count = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Consumption", f"{total_consumption:,.2f} W")
col2.metric("Average Consumption", f"{average_consumption:,.2f} W")
col3.metric("Peak Reading", f"{max_consumption:,.2f} W")
col4.metric("Readings", f"{reading_count:,}")


# -----------------------------
# SYSTEM HEALTH
# -----------------------------

st.subheader("SmartSet AI System Health")

health_score = 100

anomaly_total = len(filtered_anomalies)
high_usage_threshold = filtered_df["power_consumption"].quantile(0.75)

if anomaly_total > 20:
    health_score -= 25
elif anomaly_total > 10:
    health_score -= 15
elif anomaly_total > 5:
    health_score -= 8    

if average_consumption > high_usage_threshold:
    health_score -= 10

health_score = max(0, health_score)

if health_score >= 85:
    status = "Healthy"
elif health_score >= 65:
    status = "Monitor"
else:
    status = "Attention Needed"

health_col1, health_col2, health_col3 = st.columns(3)

health_col1.metric("System Health Score", f"{health_score}/100")
health_col2.metric("Health Status", status)
health_col3.metric("Anomalies Detected", anomaly_total)

if status == "Healthy":
    st.success("Energy usage patterns look stable for the selected household/filter.")
elif status == "Monitor":
    st.warning("Some unusual usage patterns detected. Monitor high-consuming or anomalous devices.")
else:
    st.error("Multiple anomalies detected. Review device activity and recommendations.")


st.divider()


# -----------------------------
# ENERGY OVER TIME
# -----------------------------

st.subheader("Energy Consumption Over Time")

hourly = (
    filtered_df
    .groupby("timestamp")["power_consumption"]
    .sum()
    .reset_index()
    .sort_values("timestamp")
)

fig = px.line(
    hourly,
    x="timestamp",
    y="power_consumption",
    title="Total Energy Usage Over Time"
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# TOP DEVICES
# -----------------------------

st.subheader("Top Energy Consuming Devices")

top_devices = (
    filtered_df
    .groupby(["device_id", "device_name", "device_type"])["power_consumption"]
    .sum()
    .reset_index()
    .sort_values("power_consumption", ascending=False)
    .head(10)
)

fig2 = px.bar(
    top_devices,
    x="device_name",
    y="power_consumption",
    color="device_type",
    title="Top 10 Devices by Total Consumption"
)

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# ANOMALIES
# -----------------------------

st.subheader("Anomaly Overview")

col5, col6 = st.columns(2)

col5.metric("Total Anomalies", len(filtered_anomalies))

if len(filtered_anomalies) > 0:
    col6.metric(
        "Lowest Anomaly Score",
        f"{filtered_anomalies['anomaly_score'].min():.4f}"
    )
else:
    col6.metric("Lowest Anomaly Score", "N/A")

if len(filtered_anomalies) > 0:
    anomaly_counts = (
        filtered_anomalies
        .groupby("device_type")
        .size()
        .reset_index(name="count")
    )

    fig3 = px.bar(
        anomaly_counts,
        x="device_type",
        y="count",
        title="Anomalies by Device Type"
    )

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No anomalies found for this filter.")


st.subheader("Recent Anomalies")

st.dataframe(
    filtered_anomalies
    .sort_values("detected_at", ascending=False)
    .head(20)
)


# -----------------------------
# PEAK USAGE HOURS
# -----------------------------

st.subheader("Peak Usage Hours")

peak_hours = (
    filtered_df
    .assign(hour=filtered_df["timestamp"].dt.hour)
    .groupby("hour")["power_consumption"]
    .sum()
    .reset_index()
    .sort_values("power_consumption", ascending=False)
)

fig4 = px.bar(
    peak_hours,
    x="hour",
    y="power_consumption",
    title="Total Consumption by Hour of Day"
)

st.plotly_chart(fig4, use_container_width=True)


# -----------------------------
# HOUSEHOLD RANKINGS
# -----------------------------

st.subheader("Top Households by Energy Consumption")

fig5 = px.bar(
    households,
    x="household_name",
    y="total_consumption",
    color="location",
    title="Household Energy Rankings"
)

st.plotly_chart(fig5, use_container_width=True)


# -----------------------------
# MOST ANOMALOUS DEVICES
# -----------------------------

st.subheader("Most Anomalous Devices")

most_anomalous = (
    filtered_anomalies
    .groupby(["device_name", "device_type"])
    .size()
    .reset_index(name="anomaly_count")
    .sort_values("anomaly_count", ascending=False)
    .head(10)
)

fig6 = px.bar(
    most_anomalous,
    x="device_name",
    y="anomaly_count",
    color="device_type",
    title="Devices with Most Anomalies"
)

st.plotly_chart(fig6, use_container_width=True)


# -----------------------------
# FORECASTING
# -----------------------------

st.divider()

st.subheader("Energy Forecasting")

model = joblib.load(MODEL_PATH)

forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

with forecast_col1:
    selected_hour = st.selectbox(
        "Hour of Day",
        list(range(24)),
        index=21
    )

with forecast_col2:
    day_options = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    selected_day_name = st.selectbox(
        "Day of Week",
        list(day_options.keys()),
        index=4
    )

    selected_day = day_options[selected_day_name]

with forecast_col3:
    selected_device_type = st.selectbox(
        "Forecast Device Type",
        sorted(df["device_type"].unique().tolist())
    )

if st.button("Predict Energy Consumption"):
    input_data = pd.DataFrame([{
        "hour": selected_hour,
        "day_of_week": selected_day,
        "device_type": selected_device_type,
    }])

    prediction = model.predict(input_data)[0]

    st.success(
        f"Predicted consumption for {selected_device_type} "
        f"on {selected_day_name} at {selected_hour}:00 is "
        f"{prediction:.2f} W"
    )


# -----------------------------
# DEVICE RECOMMENDATIONS
# -----------------------------

st.divider()

st.subheader("Device Recommendations")

device_options = (
    filtered_df[["device_id", "device_name", "device_type"]]
    .drop_duplicates()
    .sort_values("device_id")
)

device_label_map = {
    f"{row.device_id} - {row.device_name} ({row.device_type})": row.device_id
    for row in device_options.itertuples()
}

if len(device_label_map) > 0:
    selected_device_label = st.selectbox(
        "Select Device",
        list(device_label_map.keys())
    )

    selected_device_id = device_label_map[selected_device_label]

    device_df = filtered_df[filtered_df["device_id"] == selected_device_id]
    device_anomalies = filtered_anomalies[
        filtered_anomalies["device_id"] == selected_device_id
    ]

    avg_power = device_df["power_consumption"].mean()
    max_power = device_df["power_consumption"].max()
    anomaly_count = int(len(device_anomalies))
    device_type = device_df["device_type"].iloc[0]

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    rec_col1.metric("Average Power", f"{avg_power:.2f} W")
    rec_col2.metric("Peak Power", f"{max_power:.2f} W")
    rec_col3.metric("Anomalies", anomaly_count)

    recommendations = []

    if avg_power > device_df["power_consumption"].quantile(0.75):
        recommendations.append(
            "This device shows relatively high average usage. Consider reviewing its schedule."
        )

    if anomaly_count >= 50:
        recommendations.append(
            "This device has frequent anomalies. It may need inspection or usage review."
        )

    if device_type in ["Smart AC", "Smart Heater"]:
        recommendations.append(
            "This device is energy-intensive. Consider running it during off-peak hours."
        )

    if not recommendations:
        recommendations.append(
            "This device appears to be operating within normal usage patterns."
        )

    for rec in recommendations:
        st.info(rec)
else:
    st.info("No devices available for the selected filters.")


# -----------------------------
# RAW DATA
# -----------------------------

st.subheader("Raw Energy Readings")

st.dataframe(filtered_df.head(100))
