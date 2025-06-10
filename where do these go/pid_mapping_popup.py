
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import json
import os

PID_MAP_FILE = "pid_map.json"

def load_pid_map():
    if os.path.exists(PID_MAP_FILE):
        with open(PID_MAP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_pid_map(mapping):
    with open(PID_MAP_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

class PIDMappingPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Custom PID Mapping"
        self.size_hint = (0.75, 0.75)
        self.mapping = load_pid_map()

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.pid_input = TextInput(hint_text="PID (e.g. 0x0C)", multiline=False)
        self.label_input = TextInput(hint_text="Label (e.g. RPM)", multiline=False)
        self.unit_input = TextInput(hint_text="Unit (e.g. RPM)", multiline=False)
        self.formula_input = TextInput(hint_text="Formula (e.g. x * 0.25)", multiline=False)

        self.test_input = TextInput(hint_text="Test value (raw)", multiline=False, input_filter="float")
        self.result_label = Label(text="Result: --", size_hint=(1, 0.1))

        test_btn = Button(text="Test Formula")
        test_btn.bind(on_release=self.test_formula)

        
        export_btn = Button(text="Export PID Map")
        export_btn.bind(on_release=self.export_mapping)
        import_merge_btn = Button(text="Import (Merge)")
        import_merge_btn.bind(on_release=lambda x: self.open_import_chooser(replace=False))
        import_replace_btn = Button(text="Import (Replace)")
        import_replace_btn.bind(on_release=lambda x: self.open_import_chooser(replace=True))

        save_btn = Button(text="Save Mapping")
        save_btn.bind(on_release=self.save_mapping)

        self.layout.add_widget(Label(text="PID:"))
        self.layout.add_widget(self.pid_input)
        self.layout.add_widget(Label(text="Label:"))
        self.layout.add_widget(self.label_input)
        self.layout.add_widget(Label(text="Unit:"))
        self.layout.add_widget(self.unit_input)
        self.layout.add_widget(Label(text="Scaling Formula:"))
        self.layout.add_widget(self.formula_input)

        self.layout.add_widget(Label(text="Test Raw Value:"))
        self.layout.add_widget(self.test_input)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(test_btn)
        
        self.layout.add_widget(export_btn)
        self.layout.add_widget(import_merge_btn)
        self.layout.add_widget(import_replace_btn)
        self.layout.add_widget(save_btn)

        self.content = self.layout

    def test_formula(self, instance):
        try:
            x = float(self.test_input.text)
            result = eval(self.formula_input.text)
            self.result_label.text = f"Result: {result:.2f} {self.unit_input.text}"
        except Exception as e:
            self.result_label.text = f"Error: {e}"

    def save_mapping(self, instance):
        pid = self.pid_input.text.strip()
        if pid:
            self.mapping[pid] = {
                "label": self.label_input.text.strip(),
                "unit": self.unit_input.text.strip(),
                "formula": self.formula_input.text.strip()
            }
            save_pid_map(self.mapping)
            self.dismiss()


from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.modalview import ModalView

    def export_mapping(self, instance):
        path = "pid_map.json"
        try:
            with open(path, "w") as f:
                json.dump(self.mapping, f, indent=2)
            self.result_label.text = f"Exported to {path}"
        except Exception as e:
            self.result_label.text = f"Export failed: {e}"

    def open_import_chooser(self, replace=False):
        view = ModalView(size_hint=(0.9, 0.9))
        chooser = FileChooserIconView()
        box = BoxLayout(orientation="vertical")
        box.add_widget(chooser)
        btn = Button(text="Load and Merge" if not replace else "Load and Replace", size_hint=(1, 0.1))
        box.add_widget(btn)
        view.add_widget(box)

        def load_file(instance):
            if chooser.selection:
                self.import_mapping(chooser.selection[0], replace)
                view.dismiss()

        btn.bind(on_release=load_file)
        view.open()

    def import_mapping(self, file_path, replace=False):
        try:
            with open(file_path, "r") as f:
                new_data = json.load(f)
            if replace:
                self.mapping = new_data
            else:
                self.mapping.update(new_data)
            save_pid_map(self.mapping)
            self.result_label.text = "Import successful."
        except Exception as e:
            self.result_label.text = f"Import failed: {e}"
