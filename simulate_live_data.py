import argparse
import random
import time
from datetime import datetime

from backend.app.database import SessionLocal
from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


def generate_power(device_type, hour):
    patterns = {
        "Smart AC": {
            "morning": (900, 1500),
            "afternoon": (1800, 2600),
            "evening": (2000, 3000),
            "night": (700, 1200),
        },
        "Smart Heater": {
            "morning": (1200, 2200),
            "afternoon": (400, 900),
            "evening": (1400, 2400),
            "night": (900, 1600),
        },
        "Smart TV": {
            "morning": (20, 80),
            "afternoon": (50, 150),
            "evening": (150, 300),
            "night": (40, 120),
        },
        "Smart Light": {
            "morning": (10, 40),
            "afternoon": (5, 20),
            "evening": (40, 100),
            "night": (20, 60),
        },
        "Smart Fridge": {
            "morning": (150, 300),
            "afternoon": (180, 350),
            "evening": (180, 350),
            "night": (140, 260),
        },
    }

    if 6 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 18:
        period = "afternoon"
    elif 18 <= hour < 23:
        period = "evening"
    else:
        period = "night"

    if device_type not in patterns:
        low, high = (50, 300)
    else:
        low, high = patterns[device_type][period]

    power = random.uniform(low, high)

    if random.random() < 0.02:
        power *= random.uniform(2, 4)

    return power


def insert_live_readings(db):
    devices = db.query(Device).all()
    current_hour = datetime.utcnow().hour

    for device in devices:
        voltage = random.uniform(210, 240)
        power = generate_power(device.device_type, current_hour)
        current = power / voltage

        reading = EnergyReading(
            device_id=device.id,
            timestamp=datetime.utcnow(),
            power_consumption=power,
            voltage=voltage,
            current=current,
        )

        db.add(reading)

    db.commit()

    print(f"Inserted readings for {len(devices)} devices at {datetime.utcnow()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--cycles", type=int, default=None)

    args = parser.parse_args()

    db = SessionLocal()

    try:
        cycle_count = 0

        while True:
            insert_live_readings(db)
            cycle_count += 1

            if args.cycles is not None and cycle_count >= args.cycles:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("Live simulation stopped.")

    finally:
        db.close()


if __name__ == "__main__":
    main()


## python -m streaming.simulate_live_data --interval 60 --cycles 30