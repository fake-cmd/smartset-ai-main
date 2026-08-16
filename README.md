# SmartSet AI

SmartSet AI is an end-to-end smart-home energy intelligence platform that simulates IoT energy data, stores it in PostgreSQL, exposes analytics through FastAPI, applies machine learning for anomaly detection and forecasting, and visualizes insights through a Streamlit dashboard.

The project demonstrates practical skills across:

* Data Engineering
* Backend Development
* Machine Learning
* Time-Series Analytics
* Dashboard Development
* SQL & Database Design
* Streaming Simulation
* MLOps-style Model Serving

---

# Features

## Smart Home Simulation

* Synthetic IoT smart-home energy generation
* Context-aware energy patterns
* Morning / afternoon / evening / night usage cycles
* Live streaming simulation

## Backend APIs

* FastAPI REST APIs
* Device endpoints
* Analytics endpoints
* Recommendation endpoints
* Forecasting endpoints

## Machine Learning

* Isolation Forest anomaly detection
* Statistical threshold anomaly filtering
* Random Forest forecasting pipeline
* Feature engineering with categorical encoding

## Dashboard

* Interactive Streamlit dashboard
* Household filtering
* Device filtering
* KPI cards
* System health scoring
* Live monitoring
* Forecasting interface
* Recommendation engine

## Analytics

* Peak usage hours
* Household rankings
* Most anomalous devices
* Consumption trends
* Real-time monitoring

---
# Dashboard Screenshots

## Dashboard Overview

![Dashboard Overview](images/dashboard-overview.png)

## Forecasting

![Forecasting](images/forecasting.png)

## Energy Analytics

![Energy Consumption](images/energy-consumption-over-time.png)
![Peak hours](images/peak-usage-hours.png)

## Anomaly Detection

![Anomaly Detection](images/anomaly-overview.png)
![Anomalous Devices](images/most-anomalous-devices.png)

## Recommendations

![Recommendations](images/device-recommendations.png)

---

## Architecture Diagram

![Architecture Diagram](images/architecture-diagram.png)

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

## Data & ML

* Pandas
* Scikit-learn
* Joblib

## Dashboard

* Streamlit
* Plotly

## Utilities

* python-dotenv

---

# Project Structure

```txt
smartset-ai/
│
├── backend/
│   └── app/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       ├── database.py
│       ├── init_db.py
│       └── main.py
│
├── dashboard/
│   └── app.py
│
├── etl/
│   ├── generate_data.py
│   └── clear_readings.py
│
├── ml/
│   ├── anomaly_detection/
│   ├── forecasting/
│   └── saved_models/
│
├── streaming/
│   ├── simulate_live_data.py
│   └── run_anomaly_monitor.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Setup

## 1. Clone Repository

```bash
git clone https://github.com/akindoluakinyemi/smartset-ai
cd smartset-ai
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the root folder:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/smartset
MODEL_PATH=ml/saved_models/forecast_model.pkl
```

---

# Database Initialization

Create database tables:

```bash
python -m backend.app.init_db
```

---

# Generate Initial Dataset

```bash
python -m etl.generate_data
```

---

# Train Forecasting Model

```bash
python -m ml.forecasting.train_forecast
```

---

# Run Anomaly Detection

```bash
python -m ml.anomaly_detection.detect_anomalies
```

---

# Run FastAPI Backend

```bash
uvicorn backend.app.main:app --reload
```

Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

---

# Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Live Streaming Simulation

Run live IoT-style energy generation:

```bash
python -m streaming.simulate_live_data --interval 60
```

---

# Automated Anomaly Monitoring

Run anomaly detection periodically:

```bash
python -m streaming.run_anomaly_monitor --interval 300
```

---

# Setup Using Docker
SmartSet AI can also be run using Docker Compose.

Build and start all services:

```bash
docker-compose up --build
```
---

## 1. initilize the database in Docker
```bash
docker-compose exec backend python -m backend.app.init_db
```
---

## 2. Generate data for the Docker database
```bash
docker-compose exec backend python -m etl.generate_data
```
---

## 3. Train the forecasting model in Docker
```bash
docker-compose exec backend python -m ml.forecasting.train_forecast
```
---

## 4. Run the anomaly detection algorithm inside Docker
```bash
docker-compose exec backend python -m ml.anomaly_detection.detect_anomalies
```
---

## 5. Run the live simulation and injection of new data inside Docker
```bash
docker-compose exec backend python -m streaming.simulate_live_data --interval 60
```
---

## 6. Stop Containers
```bash
docker-compose down
```
---

# API Endpoints

## Devices

* `GET /devices/`
* `GET /devices/{device_id}`

## Households

* `GET /households/`

## Analytics

* `GET /analytics/peak-hours`
* `GET /analytics/top-households`
* `GET /analytics/most-anomalous-devices`

## Forecasting

* `POST /predict/forecast`

## Recommendations

* `GET /recommendations/device/{device_id}`

---

# Machine Learning Overview

## Anomaly Detection

The anomaly detection system uses:

* Isolation Forest
* Statistical thresholding
* Device-specific behavioral analysis

The model identifies unusual energy usage patterns using:

* power consumption
* voltage
* current
* hour of day

---

## Forecasting

The forecasting system uses:

* Random Forest Regression
* Feature preprocessing pipeline
* OneHotEncoding for categorical features

Forecasts are generated using:

* hour of day
* day of week
* device type

---

# Dashboard Features

The Streamlit dashboard includes:

* Real-time energy monitoring
* Auto-refresh functionality
* Household-level filtering
* Device-level filtering
* KPI metrics
* Health scoring
* Forecasting interface
* Device recommendations
* Anomaly visualizations
* Household rankings

---

# Example Workflow

1. Generate synthetic data
2. Train forecasting model
3. Run anomaly detection
4. Start FastAPI backend
5. Launch Streamlit dashboard
6. Start live streaming simulator
7. Monitor live analytics and anomalies

---

# Future Improvements

Potential future extensions:

* User authentication
* Kafka streaming integration
* Redis caching
* Deep learning forecasting
* WebSocket real-time updates
* MLflow model tracking
* Device clustering
* Reinforcement-learning energy optimization

---

# Purpose

This project was built to demonstrate full-stack data and machine learning engineering capabilities, including:

* relational database design
* ETL pipelines
* backend API development
* machine learning workflows
* dashboard analytics
* streaming simulation
* anomaly detection systems
* forecasting systems
* recommendation systems

---

