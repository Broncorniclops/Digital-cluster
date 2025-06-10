
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
from config_manager import AVAILABLE_PIDS

class GaugeManagerPopup(Popup):
    def __init__(self, on_save_callback, current_settings=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Gauge Configuration"
        self.size_hint = (0.9, 0.9)
        self.on_save_callback = on_save_callback
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.fields = {}
        self.preview_area = Label(text='[Live Preview]', size_hint=(1, 0.15))
        self.layout.add_widget(self.preview_area)

        form = GridLayout(cols=2, spacing=5, size_hint=(1, 0.65))

        def add_field(label, widget):
            form.add_widget(Label(text=label))
            form.add_widget(widget)

        self.fields["pid"] = Spinner(text=current_settings.get("pid", "rpm") if current_settings else "rpm",
                                     values=AVAILABLE_PIDS)
        add_field("PID", self.fields["pid"])

        self.fields["type"] = Spinner(text=current_settings.get("type", "analog") if current_settings else "analog",
                                      values=["analog", "digital", "bar"])
        add_field("Display Type", self.fields["type"])

        self.fields["label"] = TextInput(text=current_settings.get("label", "") if current_settings else "")
        add_field("Label", self.fields["label"])

        self.fields["unit"] = TextInput(text=current_settings.get("unit", "") if current_settings else "")
        add_field("Unit", self.fields["unit"])

        self.fields["min"] = TextInput(text=str(current_settings.get("min", 0)) if current_settings else "0")
        add_field("Min", self.fields["min"])

        self.fields["max"] = TextInput(text=str(current_settings.get("max", 100)) if current_settings else "100")
        add_field("Max", self.fields["max"])

        self.fields["enabled"] = CheckBox(active=current_settings.get("enabled", True) if current_settings else True)
        add_field("Enabled", self.fields["enabled"])

        self.fields["color"] = ColorPicker()
        add_field("Theme Color", self.fields["color"])

        self.fields["category"] = Spinner(text=current_settings.get("category", "General") if current_settings else "General",
                                          values=["General", "Performance", "Temperature", "Electrical", "Fuel"])
        add_field("Category", self.fields["category"])

        self.layout.add_widget(form)

        button_row = BoxLayout(size_hint=(1, 0.1))
        save_btn = Button(text="Save", on_release=self.save)
        cancel_btn = Button(text="Cancel", on_release=self.dismiss)
        button_row.add_widget(save_btn)
        button_row.add_widget(cancel_btn)
        self.layout.add_widget(button_row)

        self.content = self.layout

    def save(self, instance):
        data = {
            "pid": self.fields["pid"].text,
            "type": self.fields["type"].text,
            "label": self.fields["label"].text,
            "unit": self.fields["unit"].text,
            "min": float(self.fields["min"].text),
            "max": float(self.fields["max"].text),
            "enabled": self.fields["enabled"].active,
            "color": self.fields["color"].color,
            "category": self.fields["category"].text,
        }
        self.on_save_callback(data)
        self.dismiss()
