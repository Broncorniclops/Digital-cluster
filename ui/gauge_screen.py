
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from socket_server import start_socket_server, shutdown_flag_callback
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from sensor_manager import sensors, read_all
from config_manager import config_manager
import logging

logging.basicConfig(filename="/var/log/alert_log.txt", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

class GaugeScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.labels = {}
        self.alert_icons = {}
        self.alert_flags = {key: False for key in ["battery", "overheat", "low_oil", "check_engine"]}
        self.shutdown_flag = False

        for name in sensors:
            lbl = Label(text=f"{name}: --", font_size=18, size_hint=(.2, .05),
                        pos_hint={'x': 0, 'y': 0.9 - 0.06 * len(self.labels)})
            self.labels[name] = lbl
            self.add_widget(lbl)

        self.alert_defs = {
            "battery": ("🔋", "UPS Battery Low", lambda: sensors["ups_batt"].message if "ups_batt" in sensors else ""),
            "overheat": ("🌡️", "Engine/Trans Overheat", self.get_overheat_message),
            "low_oil": ("🛢️", "Low Oil Pressure", lambda: f"Pressure: {sensors['oil_pressure'].value:.1f} PSI"),
            "check_engine": ("🚨", "Check Engine", lambda: "See CAN diagnostic codes")
        }

        x_positions = [0.98, 0.93, 0.88, 0.83]
        for idx, (key, (icon, _, _)) in enumerate(self.alert_defs.items()):
            lbl = Label(text=icon, font_size=48, color=(1, 0, 0, 0),
                        pos_hint={'right': x_positions[idx], 'top': 0.98})
            lbl.bind(on_touch_down=self.make_touch_handler(key))
            self.alert_icons[key] = lbl
            self.add_widget(lbl)

        clear_btn = Button(text="Clear Alerts", size_hint=(.15, .08), pos_hint={"right": 0.98, "y": 0.01})
        clear_btn.bind(on_release=self.clear_alerts)
        self.add_widget(clear_btn)

        self.shutdown_msg = Label(text="Shutdown pending...", font_size=32, color=(1, 0, 0, 0),
                                  size_hint=(.6, .1), pos_hint={'center_x': 0.5, 'y': 0.85})
        self.add_widget(self.shutdown_msg)

        def on_shutdown_flag(flag):
            self.shutdown_flag = flag
        global shutdown_flag_callback
        shutdown_flag_callback = on_shutdown_flag

        start_socket_server()
        Clock.schedule_interval(self.update, 1.0 / 10)

    def make_touch_handler(self, key):
        def handler(instance, touch):
            if instance.collide_point(*touch.pos) and self.alert_flags[key]:
                _, title, msg_func = self.alert_defs[key]
                msg = msg_func()
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text=msg, font_size=20))
                close_btn = Button(text='Dismiss', size_hint=(1, 0.2))
                content.add_widget(close_btn)
                popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
                close_btn.bind(on_release=popup.dismiss)
                popup.open()
            return False
        return handler

    def get_overheat_message(self):
        msg = []
        for key in ["coolant_temp", "trans_temp"]:
            sensor = sensors.get(key)
            if sensor and sensor.value > sensor.max_val:
                msg.append(f"{sensor.name}: {sensor.value:.1f} °F (limit {sensor.max_val} °F)")
        return "\n".join(msg)

    def clear_alerts(self, instance):
        for key in self.alert_flags:
            self.alert_flags[key] = False
            self.alert_icons[key].color = (1, 0, 0, 0)
        logging.info("User cleared all active alerts.")

    def update(self, dt):
        data = read_all()
        for name, status in data.items():
            self.labels[name].text = f"{name}: {status['value']} {sensors[name].unit}"
            self.labels[name].color = (1, 0, 0, 1) if status['fault'] else (1, 1, 1, 1)

        ups = sensors.get("ups_batt")
        self.alert_flags["battery"] = ups and ups.fault and ups.message == "LOW BATTERY"
        self.shutdown_msg.color = (1, 0, 0, 1) if self.shutdown_flag else (1, 0, 0, 0)
        self.alert_icons["battery"].color = (1, 0, 0, 1) if self.alert_flags["battery"] else (1, 0, 0, 0)

        overheat = any(sensors.get(k) and sensors[k].value > sensors[k].max_val for k in ["coolant_temp", "trans_temp"])
        self.alert_flags["overheat"] = overheat
        self.alert_icons["overheat"].color = (1, 0, 0, 1) if overheat else (1, 0, 0, 0)

        oil = sensors.get("oil_pressure")
        self.alert_flags["low_oil"] = oil and oil.value < 10
        self.alert_icons["low_oil"].color = (1, 0, 0, 1) if self.alert_flags["low_oil"] else (1, 0, 0, 0)

        rpm = sensors.get("rpm")
        self.alert_flags["check_engine"] = rpm and rpm.fault
        self.alert_icons["check_engine"].color = (1, 0, 0, 1) if self.alert_flags["check_engine"] else (1, 0, 0, 0)
