import os
import socket
import subprocess
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

def is_wifi_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def perform_ota_update():
    if not is_wifi_connected():
        return show_popup("Wi-Fi Not Connected", "Connect to a network before updating.")

    result = subprocess.run(
        ["git", "-C", "/home/pi/cluster", "pull", "origin", "main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0:
        show_popup("Update Successful", result.stdout)
    else:
        show_popup("Update Failed", result.stderr)

def show_popup(title, message):
    content = BoxLayout(orientation='vertical', spacing=10)
    content.add_widget(Label(text=message))
    btn = Button(text="Close", size_hint=(1, 0.25))
    popup = Popup(title=title, content=content, size_hint=(0.75, 0.5))
    btn.bind(on_release=popup.dismiss)
    content.add_widget(btn)
    popup.open()
