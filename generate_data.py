from faker import Faker
from random import choice, uniform, random
from datetime import datetime, timedelta

from backend.app.database import SessionLocal

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


fake = Faker()


ROOMS = ["Living Room", "Kitchen", "Bedroom", "Bathroom", "Office"]

DEVICE_TYPES = [
    ("Smart AC", 1500),
    ("Smart TV", 200),
    ("Smart Light", 20),
    ("Smart Fridge", 500),
    ("Smart Heater", 1800),
]


def get_usage_multiplier(device_type: str, hour: int) -> float:
    if device_type == "Smart AC":
        if 20 <= hour <= 23:
            return uniform(0.7, 1.2)
        elif 0 <= hour <= 6:
            return uniform(0.2, 0.5)
        else:
            return uniform(0.3, 0.8)

    if device_type == "Smart TV":
        if 18 <= hour <= 23:
            return uniform(0.6, 1.0)
        else:
            return uniform(0.05, 0.3)

    if device_type == "Smart Light":
        if 18 <= hour <= 23 or 5 <= hour <= 7:
            return uniform(0.6, 1.0)
        else:
            return uniform(0.05, 0.25)

    if device_type == "Smart Fridge":
        return uniform(0.4, 0.8)

    if device_type == "Smart Heater":
        if 5 <= hour <= 8 or 19 <= hour <= 23:
            return uniform(0.6, 1.0)
        else:
            return uniform(0.05, 0.3)

    return uniform(0.2, 0.8)


def generate_power(device_type: str, power_rating: float, hour: int) -> float:
    multiplier = get_usage_multiplier(device_type, hour)
    power = power_rating * multiplier

    # occasional abnormal spike
    if random() < 0.03:
        power *= uniform(2.0, 3.5)

    return power


def clear_existing_data(db):
    db.query(Anomaly).delete()
    db.query(EnergyReading).delete()
    db.query(Device).delete()
    db.query(Room).delete()
    db.query(Household).delete()
    db.commit()


def main():
    db = SessionLocal()

    try:
        clear_existing_data(db)

        households = []

        for _ in range(5):
            household = Household(
                household_name=fake.last_name() + " Residence",
                location=fake.city(),
            )
            db.add(household)
            households.append(household)

        db.commit()

        rooms = []

        for household in households:
            for room_name in ROOMS:
                room = Room(
                    household_id=household.id,
                    room_name=room_name,
                )
                db.add(room)
                rooms.append(room)

        db.commit()

        devices = []

        for room in rooms:
            for _ in range(2):
                device_type, power_rating = choice(DEVICE_TYPES)

                device = Device(
                    room_id=room.id,
                    device_name=device_type,
                    device_type=device_type,
                    power_rating=power_rating,
                    status=True,
                )
                db.add(device)
                devices.append(device)

        db.commit()

        for device in devices:
            for hour_back in range(24 * 7):
                timestamp = datetime.utcnow() - timedelta(hours=hour_back)
                hour = timestamp.hour

                power = generate_power(
                    device.device_type,
                    device.power_rating,
                    hour,
                )

                voltage = uniform(210, 240)
                current = power / voltage

                reading = EnergyReading(
                    device_id=device.id,
                    timestamp=timestamp,
                    power_consumption=power,
                    voltage=voltage,
                    current=current,
                )

                db.add(reading)

        db.commit()

        print("Behavior-based smart home data generated successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error generating data: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()