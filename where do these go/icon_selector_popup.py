from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import os

class IconSelectorPopup(Popup):
    def __init__(self, pid, icon_dir, icon_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Select Icon for PID {pid}"
        self.size_hint = (0.7, 0.7)
        self.auto_dismiss = True
        self.icon_callback = icon_callback
        self.pid = pid

        layout = GridLayout(cols=4, spacing=10, padding=10)
        for filename in os.listdir(icon_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                icon_path = os.path.join(icon_dir, filename)
                btn = Button(size_hint=(None, None), size=(64, 64), background_normal=icon_path)
                btn.bind(on_release=lambda instance, f=filename: self.select_icon(f))
                layout.add_widget(btn)

        self.content = layout

    def select_icon(self, icon_filename):
        self.icon_callback(self.pid, icon_filename)
        self.dismiss()
