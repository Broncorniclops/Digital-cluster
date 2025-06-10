
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

# Example available PIDs, should come from can_interface or config
AVAILABLE_PIDS = [
    {"pid": "rpm", "name": "Engine RPM", "unit": "RPM", "min": 0, "max": 7000},
    {"pid": "speed", "name": "Vehicle Speed", "unit": "MPH", "min": 0, "max": 120},
    {"pid": "fuel_trim", "name": "Fuel Trim", "unit": "%", "min": -25, "max": 25},
    {"pid": "map", "name": "Manifold Pressure", "unit": "kPa", "min": 0, "max": 255},
    {"pid": "iat", "name": "Intake Temp", "unit": "°F", "min": -40, "max": 220}
]

class GaugeManagerPopup(Popup):
    def __init__(self, on_add_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Add New Gauge"
        self.size_hint = (0.75, 0.75)
        self.on_add_callback = on_add_callback

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.pid_spinner = Spinner(
            text="Select PID",
            values=[f"{p['pid']} - {p['name']}" for p in AVAILABLE_PIDS]
        )
        layout.add_widget(Label(text="PID:"))
        layout.add_widget(self.pid_spinner)

        self.display_spinner = Spinner(
            text="Display Type",
            values=["analog", "digital", "bar"]
        )
        layout.add_widget(Label(text="Display Style:"))
        layout.add_widget(self.display_spinner)

        self.label_input = TextInput(hint_text="Label (e.g. Speed)", multiline=False)
        layout.add_widget(Label(text="Gauge Label:"))
        layout.add_widget(self.label_input)

        self.unit_input = TextInput(hint_text="Unit (e.g. MPH)", multiline=False)
        layout.add_widget(Label(text="Unit:"))
        layout.add_widget(self.unit_input)

        self.min_input = TextInput(hint_text="Min Value", multiline=False, input_filter='float')
        self.max_input = TextInput(hint_text="Max Value", multiline=False, input_filter='float')
        layout.add_widget(Label(text="Min / Max Range:"))
        layout.add_widget(BoxLayout(children=[self.min_input, self.max_input]))

        add_btn = Button(text="Add Gauge")
        add_btn.bind(on_release=self.add_gauge)
        layout.add_widget(add_btn)

        self.content = layout

    def add_gauge(self, instance):
        selected_index = self.pid_spinner.values.index(self.pid_spinner.text)
        pid_info = AVAILABLE_PIDS[selected_index]

        gauge_config = {
            "pid": pid_info["pid"],
            "name": self.label_input.text or pid_info["name"],
            "unit": self.unit_input.text or pid_info["unit"],
            "display": self.display_spinner.text,
            "min": float(self.min_input.text or pid_info["min"]),
            "max": float(self.max_input.text or pid_info["max"]),
        }

        self.on_add_callback(gauge_config)
        self.dismiss()
