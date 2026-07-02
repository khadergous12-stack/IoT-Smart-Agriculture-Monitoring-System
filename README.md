# IoT-Enabled Smart Agriculture Monitoring System

An IoT platform that monitors soil moisture, temperature, humidity, and
light intensity in real time, and automates irrigation based on live
threshold logic — built as a course project demonstrating the full
sense → think → act IoT loop, from ESP32 firmware through a live dashboard.

> Built as part of an IoT coursework project under the mentorship of **Umesh Yadav sir**.

---

## Overview

This system replaces manual field checks with continuous automated
sensing. An ESP32 (or, when hardware isn't available, a Python
simulation layer) reads soil moisture, temperature, humidity, light, and
water reservoir level, applies hysteresis-based threshold logic to decide
when to irrigate, publishes everything over MQTT, and drives a
relay-controlled pump — all visible on a live standalone dashboard.

## Problem Statement

Manual irrigation monitoring is slow and inconsistent — dry soil, heat
stress, or a nearly empty reservoir can go unnoticed until crop health is
already affected. This project automates that monitoring loop so
irrigation decisions happen the moment conditions call for them, not
whenever someone next checks the field.

## IoT Concepts Demonstrated

- **Sensing** — soil moisture, temperature, humidity, light, water level
- **Edge processing** — threshold/hysteresis logic running on the ESP32 itself
- **Connectivity** — Wi-Fi + MQTT publish/subscribe
- **Cloud/visualization** — live dashboard consuming sensor + status data
- **Actuation** — relay-controlled pump acting on the edge decision
- **Data logging & reporting** — CSV logs and generated summary reports

## Hardware / Simulation Components

| Component | Role |
|---|---|
| ESP32 Dev Module | Edge compute + Wi-Fi |
| Capacitive Soil Moisture Sensor | Root-zone water content |
| DHT22 | Air temperature & humidity |
| LDR | Light intensity |
| Water Level Sensor | Reservoir level (pump safety cutoff) |
| 5V Relay Module | Pump switching |
| `python_simulation/` | Full software-only stand-in when hardware isn't available |

## Architecture

```
Sensors → ESP32 (threshold + irrigation logic) → MQTT Broker → Dashboard + CSV Log → Pump (relay)
```
Full diagram and explanation: [`docs/03_architecture.md`](docs/03_architecture.md)

## Features

- Real-time soil, climate, light, and water-level monitoring
- Hysteresis-based automatic irrigation (no pump chatter at the threshold)
- Water-level safety cutoff — pump never runs dry
- MQTT publishing (`farm/node1/data`, `farm/node1/status`, `farm/node1/alert`)
- Threshold-based alerts: low soil moisture, high temperature, low water level
- Standalone, dependency-free HTML dashboard with a soil-core-sample gauge, twin climate gauges, a 24-hour trend chart, and a live alert log
- CSV data logging + generated sensor summary report
- Parallel Python simulation layer that mirrors the firmware's exact decision logic

## Folder Structure

```
IoT-Smart-Agriculture-Monitoring-System/
│
├── arduino_code/          ESP32 firmware (.ino)
├── python_simulation/     Sensor simulator, irrigation logic, data logger, report generator, MQTT publisher
├── dashboard/             Standalone HTML live dashboard
├── data/                  Generated CSV sensor logs
├── outputs/               Generated alert log + sensor summary report
├── images/                Screenshots
├── circuit_diagram/       Circuit diagram (SVG + PNG)
├── docs/                  Full written documentation (see below)
├── README.md
├── requirements.txt
├── .gitignore
└── main.py                Simulation entry point
```

## How to Run

```bash
pip install -r requirements.txt
python main.py
```
Then open `dashboard/index.html` in any browser. Full instructions,
including the ESP32/Wokwi path: [`docs/07_how_to_run.md`](docs/07_how_to_run.md)

## Sample Output

```
Simulation complete.
  Total readings   : 288
  Pump ON events   : 14
  Alert events     : 2
  Data saved to    : data/sensor_log.csv
  Alert log saved  : outputs/alert_log.txt
  Sensor report    : outputs/sensor_report.txt
```

## Documentation

| File | Contents |
|---|---|
| [`docs/01_project_explanation.md`](docs/01_project_explanation.md) | What this is and why it matters |
| [`docs/02_tech_stack_options.md`](docs/02_tech_stack_options.md) | Easy / Intermediate / Advanced stack comparison |
| [`docs/03_architecture.md`](docs/03_architecture.md) | Full system architecture and data flow |
| [`docs/04_implementation_plan.md`](docs/04_implementation_plan.md) | Phase-by-phase build plan |
| [`docs/05_installation_setup_guide.md`](docs/05_installation_setup_guide.md) | Arduino IDE, Wokwi, Python, dashboard setup |
| [`docs/06_virtual_simulation.md`](docs/06_virtual_simulation.md) | How to simulate every scenario without hardware |
| [`docs/07_how_to_run.md`](docs/07_how_to_run.md) | Run commands + expected output |
| [`docs/08_github_upload_steps.md`](docs/08_github_upload_steps.md) | Repo setup, commit sequence, security notes |
| [`docs/09_proof_building_strategy.md`](docs/09_proof_building_strategy.md) | Day-wise build & commit plan |
| [`docs/10_interview_preparation.md`](docs/10_interview_preparation.md) | 10 interview Q&A |

## Learning Outcomes

- Designing and wiring a multi-sensor embedded system around an ESP32
- Implementing hysteresis-based control logic to avoid actuator chatter
- Structuring MQTT topics for sensor data, status, and alerts separately
- Building a dependency-free, live-updating dashboard in pure HTML/CSS/JS
- Mirroring firmware decision logic in a software simulation layer for testing without hardware
- Producing a clean, professional, GitHub-ready IoT project as a portfolio piece

---

## Arduino Firmware (`arduino_code/`)

> **Note:** This project uses a **Python virtual simulation** as the primary demo layer.
> The Arduino firmware is included for when real ESP32 hardware is available.
> You do **not** need Arduino IDE or Wokwi to run this project — `python main.py` is all you need.

Firmware for the ESP32-based hardware version of the Smart Agriculture Monitoring System.

### File
- `smart_agriculture_esp32.ino` — reads soil moisture, DHT22 temperature/humidity,
  LDR light intensity, and water level; runs the irrigation/alert logic;
  controls the relay-driven pump; and publishes JSON data over MQTT.

### Required Arduino Libraries
Install via Arduino IDE Library Manager (Sketch → Include Library → Manage Libraries):
- `DHT sensor library` (by Adafruit)
- `Adafruit Unified Sensor` (dependency of the DHT library)
- `PubSubClient` (by Nick O'Leary) — MQTT client

### Board Setup (Hardware Only)
1. Install the ESP32 board package: File → Preferences → Additional Board
   Manager URLs → add `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
2. Tools → Board → ESP32 Arduino → **ESP32 Dev Module**
3. Select the correct COM port under Tools → Port
4. Update `WIFI_SSID`, `WIFI_PASSWORD` before uploading


---

## Screenshots (`images/`)

Add your own captured screenshots here before pushing to GitHub.
See `docs/06_virtual_simulation.md` for the full list of what to capture. At minimum:

- [ ] Project folder structure screenshot
- [ ] Wokwi/Tinkercad simulation screenshot
- [ ] Serial monitor output screenshot
- [ ] `dashboard/index.html` running in a browser
- [ ] `data/sensor_log.csv` opened in a spreadsheet
- [ ] `outputs/alert_log.txt` contents
- [ ] Final GitHub repository page

Suggested filenames: `01_folder_structure.png`, `02_wokwi_simulation.png`,
`03_serial_monitor.png`, `04_dashboard.png`, `05_csv_data.png`,
`06_alert_log.png`, `07_github_repo.png`.
