
import time
import json
import os

ODOMETER_FILE = "/home/pi/digital_cluster/data/odometer.json"

class OdometerManager:
    def __init__(self):
        self.total_miles = 0.0
        self.trip_miles = 0.0
        self.last_update_time = time.time()
        self.last_speed = 0.0
        self.load()

    def load(self):
        if os.path.exists(ODOMETER_FILE):
            with open(ODOMETER_FILE, 'r') as f:
                data = json.load(f)
                self.total_miles = data.get("total_miles", 0.0)
                self.trip_miles = data.get("trip_miles", 0.0)

    def save(self):
        with open(ODOMETER_FILE, 'w') as f:
            json.dump({
                "total_miles": self.total_miles,
                "trip_miles": self.trip_miles
            }, f)

    def update(self, speed_mph):
        current_time = time.time()
        elapsed_hours = (current_time - self.last_update_time) / 3600.0
        avg_speed = (self.last_speed + speed_mph) / 2.0
        distance = avg_speed * elapsed_hours

        self.total_miles += distance
        self.trip_miles += distance

        self.last_update_time = current_time
        self.last_speed = speed_mph
        self.save()

    def reset_trip(self):
        self.trip_miles = 0.0
        self.save()

    def set_total(self, miles):
        self.total_miles = miles
        self.save()
