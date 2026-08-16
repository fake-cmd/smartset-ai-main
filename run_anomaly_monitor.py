import argparse
import time
from datetime import datetime

from ml.anomaly_detection.detect_anomalies import main as detect_anomalies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=300)

    args = parser.parse_args()

    try:
        while True:
            print(f"Running anomaly detection at {datetime.utcnow()}")
            detect_anomalies()

            print(f"Sleeping for {args.interval} seconds...")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("Anomaly monitor stopped.")


if __name__ == "__main__":
    main()