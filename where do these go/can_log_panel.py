
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os

class CANLogPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.log_path = "/var/log/can_logger.log"

        # Header
        self.add_widget(Label(text="CAN Log Viewer", font_size=24, size_hint_y=None, height=40))

        # Log display
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.log_grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.log_grid.bind(minimum_height=self.log_grid.setter('height'))
        self.scroll.add_widget(self.log_grid)
        self.add_widget(self.scroll)

        # Clear log button
        clear_btn = Button(text="Delete Log", size_hint_y=None, height=40)
        clear_btn.bind(on_release=self.clear_log)
        self.add_widget(clear_btn)

        Clock.schedule_interval(self.refresh_log, 5)

    def refresh_log(self, dt):
        self.log_grid.clear_widgets()
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r") as f:
                    lines = f.readlines()[-50:]  # show last 50 entries
                    for line in lines:
                        self.log_grid.add_widget(Label(text=line.strip(), font_size=14, size_hint_y=None, height=30))
            except Exception as e:
                self.log_grid.add_widget(Label(text=f"Error reading log: {e}", color=(1, 0, 0, 1)))

    def clear_log(self, instance):
        if os.path.exists(self.log_path):
            try:
                open(self.log_path, 'w').close()
                self.refresh_log(0)
            except Exception as e:
                self.log_grid.add_widget(Label(text=f"Error clearing log: {e}", color=(1, 0, 0, 1)))
