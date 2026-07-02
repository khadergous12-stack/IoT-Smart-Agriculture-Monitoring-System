# Installation / Setup Guide

## 1. Arduino IDE Setup

1. Download Arduino IDE 2.x from https://www.arduino.cc/en/software
2. Open **File → Preferences**, add this to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Open **Tools → Board → Boards Manager**, search "esp32", install the Espressif package
4. Select **Tools → Board → ESP32 Arduino → ESP32 Dev Module**

## 2. Required Libraries

Install via **Sketch → Include Library → Manage Libraries**:
- `DHT sensor library` (Adafruit)
- `Adafruit Unified Sensor`
- `PubSubClient`

## 3. Wokwi Simulation Setup (no hardware needed)

1. Go to https://wokwi.com and create a new ESP32 project
2. Paste the contents of `arduino_code/smart_agriculture_esp32.ino`
3. Add virtual components: DHT22, two potentiometers (standing in for soil
   moisture and water level ADC inputs), an LDR, and a relay module
4. Wire them to the pins listed in `arduino_code/README.md`
5. Click the green Play button to run the simulation and watch Serial Monitor output

## 4. Python Setup (simulation layer)

**Windows / macOS / Linux — identical commands:**
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

This runs a full 24-hour simulated field session and writes:
- `data/sensor_log.csv`
- `outputs/alert_log.txt`
- `outputs/sensor_report.txt`

## 5. Dashboard Setup

No build step required — it's a single static file.
```bash
# Just open it directly:
open dashboard/index.html          # macOS
start dashboard/index.html         # Windows
xdg-open dashboard/index.html      # Linux
```
Or deploy it directly to Netlify by dragging the `dashboard/` folder into
the Netlify dashboard.

## 6. MQTT Broker Setup (optional, for live hardware)

No account needed — this project uses the public test broker
`broker.hivemq.com` on port `1883`. For production use, swap in a private
broker (Mosquitto self-hosted, or AWS IoT Core) and update
`MQTT_BROKER` in the firmware.
