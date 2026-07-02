# How to Run This Project

## Run the Arduino / Wokwi Simulation
1. Open `arduino_code/smart_agriculture_esp32.ino` in Arduino IDE (or paste into a Wokwi ESP32 project)
2. Set `WIFI_SSID` and `WIFI_PASSWORD` (real hardware only — not needed in Wokwi)
3. Upload / press Play
4. Open Serial Monitor at **115200 baud**

Expected serial output:
```
Connecting to Wi-Fi..... connected.
192.168.1.42
Connecting to MQTT broker...connected.
Temp: 26.4 C | Hum: 58.2 % | Soil: 2130 | Light: 2870 | Water: 74.5 % | Pump: OFF
Temp: 26.5 C | Hum: 57.9 % | Soil: 2098 | Light: 2910 | Water: 74.4 % | Pump: OFF
```

## Run the Python Simulation
```bash
python main.py
```
Expected console output:
```
IoT-Enabled Smart Agriculture Monitoring System — Simulation
============================================================
Simulating 24 hours of field data (5-minute interval)...

Simulation complete.
  Total readings   : 288
  Pump ON events   : 14
  Alert events     : 2
  Data saved to    : data/sensor_log.csv
  Alert log saved  : outputs/alert_log.txt
  Sensor report    : outputs/sensor_report.txt
```

## View the Dashboard
Open `dashboard/index.html` in any modern browser — no server required.

## Sample Alert Messages
```
[2026-07-01T13:45:35] LOW_SOIL_MOISTURE (soil=1495, temp=30.9C, water=78.0%)
[2026-07-02T04:35:35] LOW_SOIL_MOISTURE (soil=1499, temp=19.9C, water=71.7%)
```
