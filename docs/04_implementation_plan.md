# Implementation Plan (Phase-Wise)

### Phase 1 — Setup
**What:** Install Arduino IDE / Python, set up the project folder structure.
**Why:** A clean, GitHub-ready structure from day one avoids painful reorganizing later.
**Expected output:** Empty but organized repository skeleton.
**Common mistake:** Starting to write code before deciding on folder structure.

### Phase 2 — Sensor Selection
**What:** Choose soil moisture, DHT22, LDR, and water level sensors; confirm pin requirements.
**Why:** Wrong sensor choice (e.g. resistive vs capacitive soil sensor) affects long-term reliability.
**Expected output:** Finalized bill of materials and pinout plan.
**Common mistake:** Ignoring that resistive soil sensors corrode quickly — this project uses capacitive.

### Phase 3 — Circuit Design / Simulation
**What:** Wire the sensors to the ESP32 (or model in Wokwi) and design the circuit diagram.
**Why:** Confirms pin mapping before code is written against it.
**Expected output:** `circuit_diagram/circuit_diagram.png`
**Common mistake:** Using pins that don't support ADC on the ESP32 (only ADC1 pins are safe while Wi-Fi is active).

### Phase 4 — Sensor Data Reading
**What:** Write firmware to read all four sensors and print to Serial Monitor.
**Why:** Validates wiring and sensor function before adding any logic on top.
**Expected output:** Live serial readings every few seconds.
**Common mistake:** Not handling `NaN` reads from the DHT22 (happens occasionally — must be checked, not ignored).

### Phase 5 — Threshold Logic
**What:** Implement dry/wet soil thresholds, high-temperature threshold, low-water threshold.
**Why:** This is the decision-making core of the whole system.
**Expected output:** Correct pump ON/OFF decisions against test values.
**Common mistake:** Using a single threshold instead of two (causes rapid pump cycling — see hysteresis note in `03_architecture.md`).

### Phase 6 — Pump / Relay Control Simulation
**What:** Wire and test the relay, confirm active-low/active-high behavior for the specific module used.
**Why:** Relay modules vary — some are active-low, some active-high. Getting this backwards means the pump runs *inverted*.
**Expected output:** Pump switches correctly with irrigation logic.
**Common mistake:** Assuming all relay boards behave the same way without testing.

### Phase 7 — Dashboard Integration
**What:** Build the standalone HTML dashboard (`dashboard/index.html`).
**Why:** Turns raw numbers into something a farmer can actually read at a glance.
**Expected output:** Live-updating gauges, trend chart, alert log, pump status.
**Common mistake:** Building a dashboard that only shows current values with no historical trend.

### Phase 8 — Alert Generation
**What:** Publish MQTT alert messages when thresholds are crossed.
**Why:** Alerts are what make the system actionable, not just observational.
**Expected output:** `LOW_SOIL_MOISTURE`, `HIGH_TEMPERATURE`, `LOW_WATER_LEVEL` events.
**Common mistake:** Flooding the alert channel with duplicate messages every cycle instead of on state change.

### Phase 9 — Data Logging
**What:** Log every reading to CSV, generate a summary report.
**Why:** Historical data lets you evaluate irrigation efficiency over time.
**Expected output:** `data/sensor_log.csv`, `outputs/sensor_report.txt`
**Common mistake:** Not including a timestamp column, making the log useless for trend analysis.

### Phase 10 — GitHub Upload
**What:** Push the repo, write the README, capture screenshots.
**Why:** This is the proof-of-work deliverable for the course.
**Expected output:** Public GitHub repository with clean commit history.
**Common mistake:** Committing secrets (Wi-Fi password, API keys) directly into the firmware file.
