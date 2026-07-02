"""
data_logger.py
---------------
Writes simulated sensor + irrigation-decision records to CSV, and produces
a simple text alert log, matching the "data logging" phase of the project.
"""

import csv
import os


FIELDNAMES = [
    "timestamp",
    "soil_moisture_raw",
    "temperature_c",
    "humidity_pct",
    "light_raw",
    "water_level_pct",
    "pump_status",
    "alerts",
]


def write_csv(records: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in records:
            row = {k: r.get(k, "") for k in FIELDNAMES}
            row["alerts"] = "|".join(r.get("alerts", []))
            writer.writerow(row)


def write_alert_log(records: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("Smart Agriculture Monitoring System - Alert Log\n")
        f.write("=" * 50 + "\n\n")
        count = 0
        for r in records:
            if r.get("alerts"):
                count += 1
                f.write(f"[{r['timestamp']}] {', '.join(r['alerts'])} "
                        f"(soil={r['soil_moisture_raw']}, temp={r['temperature_c']}C, "
                        f"water={r['water_level_pct']}%)\n")
        f.write(f"\nTotal alert events: {count}\n")


if __name__ == "__main__":
    demo = [{
        "timestamp": "2026-07-02T06:00:00",
        "soil_moisture_raw": 1200,
        "temperature_c": 22.1,
        "humidity_pct": 60,
        "light_raw": 100,
        "water_level_pct": 70,
        "pump_status": "PumpON",
        "alerts": ["LOW_SOIL_MOISTURE"],
    }]
    write_csv(demo, "../data/demo.csv")
    write_alert_log(demo, "../outputs/demo_alerts.txt")
