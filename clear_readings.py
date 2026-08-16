from backend.app.database import SessionLocal
from backend.app.models.anomaly import Anomaly
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device


def main():
    db = SessionLocal()

    try:
        db.query(Anomaly).delete()
        db.query(EnergyReading).delete()
        db.commit()

        print("Energy readings and anomalies cleared successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error clearing data: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()