"""
irrigation_logic.py
--------------------
Threshold comparison, pump ON/OFF decision-making, and alert generation
for the Smart Agriculture Monitoring System.

Mirrors the logic running on the ESP32 firmware (see arduino_code/) so the
Python simulation and real hardware produce identical decisions given the
same sensor inputs.
"""

# Thresholds (tune per crop / soil type)
SOIL_DRY_THRESHOLD = 1500        # below this raw ADC value = dry soil -> irrigate
SOIL_WET_THRESHOLD = 2600        # above this = sufficiently moist -> stop irrigating
TEMP_HIGH_ALERT_C = 38.0
WATER_LEVEL_LOW_PCT = 15.0
LIGHT_LOW_RAW = 300              # below this during daytime hours = shading/cloud issue


class IrrigationController:
    """Hysteresis-based pump control to avoid rapid ON/OFF cycling."""

    def __init__(self):
        self.pump_on = False

    def evaluate(self, reading: dict) -> dict:
        soil = reading["soil_moisture_raw"]
        temp = reading["temperature_c"]
        water_level = reading["water_level_pct"]

        alerts = []

        # --- Irrigation decision (hysteresis) ---
        if water_level <= WATER_LEVEL_LOW_PCT:
            # Never run pump dry
            self.pump_on = False
            alerts.append("LOW_WATER_LEVEL")
        elif soil < SOIL_DRY_THRESHOLD:
            self.pump_on = True
        elif soil > SOIL_WET_THRESHOLD:
            self.pump_on = False

        # --- Alerts ---
        if soil < SOIL_DRY_THRESHOLD:
            alerts.append("LOW_SOIL_MOISTURE")
        if temp >= TEMP_HIGH_ALERT_C:
            alerts.append("HIGH_TEMPERATURE")

        return {
            "pump_on": self.pump_on,
            "pump_status": "PumpON" if self.pump_on else "PumpOFF",
            "alerts": alerts,
        }


if __name__ == "__main__":
    controller = IrrigationController()
    sample = {"soil_moisture_raw": 1200, "temperature_c": 39.5, "water_level_pct": 40}
    print(controller.evaluate(sample))
