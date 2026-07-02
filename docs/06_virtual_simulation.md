# Virtual Simulation Guide

Since real hardware may not be available, this project can be fully
demonstrated through simulation. Here's how to exercise every scenario:

## Simulate Dry Soil
In `python_simulation/sensor_simulator.py`, lower the starting
`self.soil_moisture` value (e.g. to `1200`) and re-run `main.py`. You'll
see the pump switch `PumpON` almost immediately in the console/CSV output.

## Simulate Wet Soil
Set `self.soil_moisture` to `3200` and re-run — the pump should stay
`PumpOFF` for the full session since it never crosses the dry threshold.

## Simulate High Temperature
In `irrigation_logic.py`, temporarily lower `TEMP_HIGH_ALERT_C` to `25.0`
and re-run — you'll see `HIGH_TEMPERATURE` alerts appear in
`outputs/alert_log.txt` during the simulated daytime hours.

## Simulate Low Water Level
Set `self.water_tank_level = 10.0` in `sensor_simulator.py` and re-run —
the controller will refuse to run the pump even if soil is dry, and log
`LOW_WATER_LEVEL` alerts instead.

## Simulate Pump ON/OFF Cycling
Run the default 24-hour session (`python main.py`) — the natural
day/night evaporation curve will dry the soil out during the afternoon,
triggering a realistic pump ON→OFF cycle you can see directly in
`data/sensor_log.csv`.

## Viewing Dashboard Values
Open `dashboard/index.html` — the same day/night simulation logic runs
live in-browser, so the gauges, soil core sample, and trend chart update
every 3 seconds without needing the Python layer running at all.

## Screenshots to Capture
- Wokwi circuit simulation running, Serial Monitor visible
- Terminal output of `python main.py` showing the run summary
- `dashboard/index.html` open in a browser, showing live gauges
- `data/sensor_log.csv` opened in a spreadsheet app
- `outputs/alert_log.txt` and `outputs/sensor_report.txt` contents
- The final GitHub repository page after pushing
