# dtc_viewer_panel.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from dtc_manager import read_dtcs, clear_dtcs

class DTCViewerPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.dtc_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.dtc_list.bind(minimum_height=self.dtc_list.setter('height'))

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.scroll.add_widget(self.dtc_list)

        self.add_widget(Label(text="Diagnostic Trouble Codes", font_size=22, size_hint=(1, 0.1)))
        self.add_widget(self.scroll)

        button_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        refresh_btn = Button(text="Refresh")
        refresh_btn.bind(on_release=self.refresh)
        clear_btn = Button(text="Clear DTCs")
        clear_btn.bind(on_release=self.clear_dtcs)

        button_bar.add_widget(refresh_btn)
        button_bar.add_widget(clear_btn)
        self.add_widget(button_bar)

        self.refresh()

    def refresh(self, instance=None):
        self.dtc_list.clear_widgets()
        dtcs = read_dtcs()
        if dtcs:
            for code in dtcs:
                desc = self.get_description(code)
                self.dtc_list.add_widget(Label(text=f"{code} - {desc}", size_hint_y=None, height=30))
        else:
            self.dtc_list.add_widget(Label(text="No DTCs Found", size_hint_y=None, height=30))

    def clear_dtcs(self, instance):
        success = clear_dtcs()
        if success:
            self.show_popup("DTCs Cleared", "Trouble codes successfully cleared.")
        else:
            self.show_popup("Error", "Failed to clear DTCs.")
        self.refresh()

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=message))
        btn = Button(text="Close", size_hint=(1, 0.3))
        popup = Popup(title=title, content=box, size_hint=(0.6, 0.4))
        btn.bind(on_release=popup.dismiss)
        box.add_widget(btn)
        popup.open()

    def get_description(self, code):
        # Basic placeholder for DTC meaning
        known = {
            "P0300": "Random/Multiple Cylinder Misfire Detected",
            "P0171": "System Too Lean (Bank 1)",
            "P0420": "Catalyst System Efficiency Below Threshold"
        }
        return known.get(code, "Unknown Fault Code")
