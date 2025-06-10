
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from dtc_manager import get_dtc_list, clear_dtc

class DTCViewerPanel(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="DTC Viewer", size_hint=(0.8, 0.8), **kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.dtc_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.dtc_container.bind(minimum_height=self.dtc_container.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.dtc_container)
        layout.add_widget(scroll)

        clear_btn = Button(text='Clear DTCs', size_hint=(1, 0.1))
        clear_btn.bind(on_release=self.clear_dtcs)
        layout.add_widget(clear_btn)

        close_btn = Button(text='Close', size_hint=(1, 0.1))
        close_btn.bind(on_release=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout
        self.populate_dtc_list()

    def populate_dtc_list(self):
        self.dtc_container.clear_widgets()
        dtcs = get_dtc_list()
        if not dtcs:
            self.dtc_container.add_widget(Label(text="No DTCs Found", size_hint_y=None, height=40))
        else:
            for code, description in dtcs:
                self.dtc_container.add_widget(Label(text=f"{code}: {description}", size_hint_y=None, height=40))

    def clear_dtcs(self, instance):
        clear_dtc()
        self.populate_dtc_list()
