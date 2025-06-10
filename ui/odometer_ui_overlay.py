
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from modules.odometer_manager import OdometerManager
from sensor_manager import sensors

class OdometerGaugeOverlay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.odo_mgr = OdometerManager()

        self.odometer_label = Label(text="ODO: 0.0 mi", font_size=18,
                                    size_hint=(.2, .05), pos_hint={'x': 0.75, 'y': 0.01})
        self.trip_label = Label(text="TRIP: 0.0 mi", font_size=18,
                                size_hint=(.2, .05), pos_hint={'x': 0.75, 'y': 0.06})

        self.add_widget(self.odometer_label)
        self.add_widget(self.trip_label)

        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        speed = sensors.get("speed")
        rpm = sensors.get("rpm")
        if speed and rpm:
            self.odo_mgr.update(rpm.value, speed.value)
        self.odometer_label.text = f"ODO: {self.odo_mgr.total_miles:.1f} mi"
        self.trip_label.text = f"TRIP: {self.odo_mgr.trip_miles:.1f} mi"

    def reset_trip(self):
        self.odo_mgr.reset_trip()

    def set_odometer(self, new_value):
        self.odo_mgr.set_total_miles(new_value)
