
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os
import logging

logging.basicConfig(filename="/var/log/maintenance.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

LOG_PATHS = {
    "CAN Log": "/var/log/can_logger.log",
    "Alert Log": "/var/log/alert_log.txt",
    "DTC Log": "/var/log/dtc_log.txt",
    "Maintenance Log": "/var/log/maintenance.log"
}

class LogCleanupPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.checkboxes = {}

        self.add_widget(Label(text="Select Logs to Delete", font_size=20, size_hint_y=None, height=40))

        scroll = ScrollView(size_hint=(1, 0.7))
        grid = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))

        for name, path in LOG_PATHS.items():
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            chk = CheckBox(size_hint=(0.1, 1))
            lbl = Label(text=name, halign="left", valign="middle", size_hint=(0.9, 1))
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(chk)
            row.add_widget(lbl)
            grid.add_widget(row)
            self.checkboxes[name] = chk

        scroll.add_widget(grid)
        self.add_widget(scroll)

        # Select All toggle
        select_all_btn = Button(text="Select All", size_hint_y=None, height=40)
        select_all_btn.bind(on_release=self.toggle_all)
        self.add_widget(select_all_btn)

        # Delete selected
        delete_btn = Button(text="Delete Selected Logs", size_hint_y=None, height=40)
        delete_btn.bind(on_release=self.delete_selected)
        self.add_widget(delete_btn)

    def toggle_all(self, instance):
        all_selected = all(cb.active for cb in self.checkboxes.values())
        for cb in self.checkboxes.values():
            cb.active = not all_selected

    def delete_selected(self, instance):
        for name, chk in self.checkboxes.items():
            if chk.active:
                path = LOG_PATHS.get(name)
                try:
                    if os.path.exists(path):
                        open(path, "w").close()
                        logging.info(f"Deleted {name}: {path}")
                except Exception as e:
                    logging.error(f"Failed to delete {name}: {e}")
