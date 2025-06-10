import time
import json
from pathlib import Path

class Odometer:
    def __init__(self, data_path="config/odometer_data.json"):
        self.data_path = Path(data_path)
        self.total_miles = 0.0
        self.trip_miles = 0.0
        self.last_update = time.time()
        self._load_data()

    def _load_data(self):
        if self.data_path.exists():
            try:
                with self.data_path.open("r") as f:
                    data = json.load(f)
                    self.total_miles = data.get("total_miles", 0.0)
                    self.trip_miles = data.get("trip_miles", 0.0)
            except Exception:
                self.total_miles = 0.0
                self.trip_miles = 0.0

    def _save_data(self):
        data = {
            "total_miles": round(self.total_miles, 2),
            "trip_miles": round(self.trip_miles, 2)
        }
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_path.open("w") as f:
            json.dump(data, f)

    def update(self, speed_mph):
        current_time = time.time()
        elapsed = current_time - self.last_update
        self.last_update = current_time
        miles = (speed_mph * elapsed) / 3600.0
        self.total_miles += miles
        self.trip_miles += miles
        self._save_data()

    def reset_trip(self):
        self.trip_miles = 0.0
        self._save_data()

    def get_readings(self):
        return {
            "total_miles": round(self.total_miles, 2),
            "trip_miles": round(self.trip_miles, 2)
        }