"""
sensor_simulator.py
--------------------
Generates realistic virtual sensor readings for the Smart Agriculture
Monitoring System when real ESP32 hardware is not available.

Simulates:
    - Soil Moisture   (0-4095, ADC-style raw reading, capacitive sensor)
    - Temperature      (deg C, DHT22 range)
    - Humidity         (%RH, DHT22 range)
    - Light Intensity  (0-4095, LDR raw reading)
    - Water Level      (%, ultrasonic/float sensor)

Readings follow a 24-hour day/night cycle so the dashboard and irrigation
logic behave like a real greenhouse / open field deployment.
"""

import math
import random
from datetime import datetime, timedelta


class FieldSensorSimulator:
    """Stateful simulator: soil dries out over time and resets on 'irrigation'."""

    def __init__(self, seed: int | None = 42):
        self.rng = random.Random(seed)
        self.soil_moisture = 2600          # start moist (higher = wetter for this sensor)
        self.water_tank_level = 78.0       # percent
        self.elapsed_minutes = 0

    def _hour_fraction(self, timestamp: datetime) -> float:
        return timestamp.hour + timestamp.minute / 60.0

    def _ambient_temperature(self, hour: float) -> float:
        # Peaks mid-afternoon (~15:00), lowest before dawn (~05:00)
        base = 24.0
        swing = 7.5
        return base + swing * math.sin((hour - 7) / 24 * 2 * math.pi)

    def _ambient_humidity(self, hour: float, temp: float) -> float:
        # Humidity inversely related to temperature
        base = 65.0
        swing = 15.0
        return max(30.0, min(95.0, base - swing * math.sin((hour - 7) / 24 * 2 * math.pi) + self.rng.uniform(-2, 2)))

    def _light_intensity(self, hour: float) -> int:
        # Daylight curve, 0 at night, peak at noon
        if 6 <= hour <= 18.5:
            daylight = math.sin((hour - 6) / 12.5 * math.pi)
            raw = int(3900 * max(0.0, daylight))
        else:
            raw = 0
        return max(0, min(4095, raw + self.rng.randint(-40, 40)))

    def step(self, timestamp: datetime, pump_active: bool) -> dict:
        hour = self._hour_fraction(timestamp)
        temperature = round(self._ambient_temperature(hour) + self.rng.uniform(-0.6, 0.6), 1)
        humidity = round(self._ambient_humidity(hour, temperature), 1)
        light = self._light_intensity(hour)

        # Soil dries faster in heat/daylight, recovers when pump runs
        evap_rate = 4.0 + (light / 4095) * 6.0 + max(0, temperature - 24) * 0.8
        if pump_active:
            self.soil_moisture = min(3600, self.soil_moisture + 180)
            self.water_tank_level = max(0.0, self.water_tank_level - 0.9)
        else:
            self.soil_moisture = max(900, self.soil_moisture - evap_rate - self.rng.uniform(0, 3))

        # Tank slowly refills to simulate periodic manual refill/rain
        if self.rng.random() < 0.002:
            self.water_tank_level = min(100.0, self.water_tank_level + self.rng.uniform(10, 25))

        self.elapsed_minutes += 5

        return {
            "timestamp": timestamp.isoformat(timespec="seconds"),
            "soil_moisture_raw": int(self.soil_moisture),
            "temperature_c": temperature,
            "humidity_pct": humidity,
            "light_raw": light,
            "water_level_pct": round(self.water_tank_level, 1),
        }


def generate_series(hours: int = 24, interval_minutes: int = 5, start: datetime | None = None):
    """Generate a full time series of sensor + irrigation-decision records."""
    from irrigation_logic import IrrigationController

    sim = FieldSensorSimulator()
    controller = IrrigationController()
    start = start or (datetime.now() - timedelta(hours=hours))

    records = []
    pump_active = False
    steps = int((hours * 60) / interval_minutes)

    for i in range(steps):
        ts = start + timedelta(minutes=i * interval_minutes)
        reading = sim.step(ts, pump_active)
        decision = controller.evaluate(reading)
        pump_active = decision["pump_on"]
        reading.update(decision)
        records.append(reading)

    return records


if __name__ == "__main__":
    data = generate_series(hours=24)
    print(f"Generated {len(data)} simulated readings.")
    print(data[0])
    print(data[-1])
