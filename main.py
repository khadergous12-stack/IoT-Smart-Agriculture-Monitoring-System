"""
main.py
-------
Entry point for the IoT-Enabled Smart Agriculture Monitoring System
(virtual simulation mode).

Runs a 24-hour simulated field session:
    1. Generates sensor readings every 5 simulated minutes
    2. Applies irrigation threshold logic (pump ON/OFF + alerts)
    3. Publishes each reading (console-mode MQTT by default)
    4. Logs everything to data/sensor_log.csv and outputs/alert_log.txt
    5. Prints a short run summary

Run:
    python main.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python_simulation"))

from sensor_simulator import generate_series
from data_logger import write_csv, write_alert_log
from mqtt_publisher import MQTTPublisher
from report_generator import generate_report


DATA_CSV = os.path.join("data", "sensor_log.csv")
ALERT_LOG = os.path.join("outputs", "alert_log.txt")
SENSOR_REPORT = os.path.join("outputs", "sensor_report.txt")


def run(hours: int = 24, publish: bool = False):
    print("IoT-Enabled Smart Agriculture Monitoring System — Simulation")
    print("=" * 60)
    print(f"Simulating {hours} hours of field data (5-minute interval)...\n")

    records = generate_series(hours=hours, interval_minutes=5)

    publisher = MQTTPublisher(enabled=publish)
    if publish:
        for r in records:
            publisher.publish_reading(r)
    else:
        print(f"[MQTT] Console mode disabled for bulk run — {len(records)} readings ready to publish.")
        print(f"[MQTT] Sample payload: {records[0]}")

    write_csv(records, DATA_CSV)
    write_alert_log(records, ALERT_LOG)
    generate_report(DATA_CSV, SENSOR_REPORT)

    pump_on_count = sum(1 for r in records if r["pump_status"] == "PumpON")
    alert_count = sum(1 for r in records if r["alerts"])

    print("\nSimulation complete.")
    print(f"  Total readings   : {len(records)}")
    print(f"  Pump ON events   : {pump_on_count}")
    print(f"  Alert events     : {alert_count}")
    print(f"  Data saved to    : {DATA_CSV}")
    print(f"  Alert log saved  : {ALERT_LOG}")
    print(f"  Sensor report    : {SENSOR_REPORT}")


if __name__ == "__main__":
    run(hours=24, publish=False)
