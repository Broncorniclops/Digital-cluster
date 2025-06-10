import socket
import configparser
import os

CONFIG_PATH = "/home/pi/cluster/settings.ini"

def is_wifi_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        config["OTA"] = {"auto_updates": "true"}
        with open(CONFIG_PATH, "w") as f:
            config.write(f)
    else:
        config.read(CONFIG_PATH)
    return config

def auto_update_enabled():
    config = load_config()
    enabled = config.getboolean("OTA", "auto_updates", fallback=True)
    return enabled and is_wifi_connected()

def toggle_auto_update():
    config = load_config()
    current = config.getboolean("OTA", "auto_updates", fallback=True)
    config["OTA"]["auto_updates"] = str(not current).lower()
    with open(CONFIG_PATH, "w") as f:
        config.write(f)
    return not current
