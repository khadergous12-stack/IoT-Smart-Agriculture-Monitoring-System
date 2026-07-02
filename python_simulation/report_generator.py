"""
report_generator.py
--------------------
Reads data/sensor_log.csv and produces a plain-text summary report
(outputs/sensor_report.txt) with min/max/avg statistics — the "sensor
report" output referenced in the project spec.
"""

import csv
import os
import statistics as stats


def generate_report(csv_path: str, out_path: str) -> None:
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    soil = [int(r["soil_moisture_raw"]) for r in rows]
    temp = [float(r["temperature_c"]) for r in rows]
    hum = [float(r["humidity_pct"]) for r in rows]
    light = [int(r["light_raw"]) for r in rows]
    water = [float(r["water_level_pct"]) for r in rows]
    pump_on = sum(1 for r in rows if r["pump_status"] == "PumpON")
    alerts = sum(1 for r in rows if r["alerts"])

    lines = [
        "IoT-Enabled Smart Agriculture Monitoring System - Sensor Report",
        "=" * 65,
        f"Records analyzed : {len(rows)}",
        f"Period           : {rows[0]['timestamp']}  to  {rows[-1]['timestamp']}",
        "",
        "Soil Moisture (raw ADC, higher = wetter)",
        f"   min={min(soil)}  max={max(soil)}  avg={round(stats.mean(soil),1)}",
        "",
        "Temperature (C)",
        f"   min={min(temp)}  max={max(temp)}  avg={round(stats.mean(temp),1)}",
        "",
        "Humidity (%RH)",
        f"   min={min(hum)}  max={max(hum)}  avg={round(stats.mean(hum),1)}",
        "",
        "Light Intensity (raw ADC)",
        f"   min={min(light)}  max={max(light)}  avg={round(stats.mean(light),1)}",
        "",
        "Water Tank Level (%)",
        f"   min={min(water)}  max={max(water)}  avg={round(stats.mean(water),1)}",
        "",
        f"Pump ON readings : {pump_on} / {len(rows)}",
        f"Alert events     : {alerts}",
    ]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    generate_report(
        os.path.join("..", "data", "sensor_log.csv"),
        os.path.join("..", "outputs", "sensor_report.txt"),
    )
