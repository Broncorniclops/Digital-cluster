from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from sensor_manager import sensors, read_all
from odometer import OdometerManager
import logging

logging.basicConfig(filename="/var/log/alert_log.txt", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class GaugeScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.labels = {}
        self.alert_icons = {}
        self.alert_flags = {key: False for key in ["battery", "overheat", "low_oil", "check_engine"]}
        self.odometer_manager = OdometerManager()

        for name in sensors:
            lbl = Label(text=f"{name}: --", font_size=18, size_hint=(.2, .05),
                        pos_hint={'x': 0, 'y': 0.9 - 0.06 * len(self.labels)})
            self.labels[name] = lbl
            self.add_widget(lbl)

        self.odo_label = Label(text="Odometer: 0.0 mi", font_size=20, size_hint=(.3, .05), pos_hint={'x': 0.65, 'y': 0.85})
        self.trip_label = Label(text="Trip: 0.0 mi", font_size=20, size_hint=(.3, .05), pos_hint={'x': 0.65, 'y': 0.79})
        self.add_widget(self.odo_label)
        self.add_widget(self.trip_label)

        reset_btn = Button(text="Reset Trip", size_hint=(.1, .05), pos_hint={"x": 0.88, "y": 0.79})
        reset_btn.bind(on_release=self.reset_trip)
        self.add_widget(reset_btn)

        Clock.schedule_interval(self.update, 1.0 / 10)

    def reset_trip(self, instance):
        self.odometer_manager.reset_trip()
        logging.info("Trip meter reset.")

    def update(self, dt):
        data = read_all()
        for name, status in data.items():
            self.labels[name].text = f"{name}: {status['value']} {sensors[name].unit}"
            self.labels[name].color = (1, 0, 0, 1) if status['fault'] else (1, 1, 1, 1)

        speed = sensors.get("speed")
        if speed and speed.value >= 0:
            self.odometer_manager.update(speed.value, dt)

        self.odo_label.text = f"Odometer: {self.odometer_manager.odometer:.1f} mi"
        self.trip_label.text = f"Trip: {self.odometer_manager.trip_meter:.1f} mi"