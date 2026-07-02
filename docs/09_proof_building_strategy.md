# Day-Wise Proof Building Strategy

### Day 1 — Setup & Sensor Planning
- Create repo, folder structure, README skeleton
- Finalize sensor list and pin mapping
- **Commit:** `"Initial commit: project structure and README"`
- **Screenshot:** empty project folder tree

### Day 2 — Circuit Simulation
- Build the circuit in Wokwi / design `circuit_diagram.svg`
- **Commit:** `"Add circuit diagram"`
- **Screenshot:** Wokwi canvas + exported circuit diagram PNG

### Day 3 — Sensor Reading
- Write and test ESP32 firmware sensor-reading loop
- **Commit:** `"Add ESP32 firmware for sensor reading and irrigation control"`
- **Screenshot:** Serial Monitor showing live readings

### Day 4 — Threshold & Pump Logic
- Implement hysteresis irrigation logic in both firmware and Python
- **Commit:** `"Add irrigation threshold logic with hysteresis"`
- **Screenshot:** terminal output showing pump ON/OFF transitions

### Day 5 — Dashboard / Alerts
- Build `dashboard/index.html`, wire up alert publishing
- **Commit:** `"Add standalone HTML dashboard"`
- **Screenshot:** dashboard open in browser showing live gauges

### Day 6 — Data Logging & Documentation
- Generate `sensor_log.csv`, `sensor_report.txt`, finish docs
- **Commit:** `"Add data logging, sensor report, and full documentation"`
- **Screenshot:** CSV opened in spreadsheet app + final GitHub repo page
