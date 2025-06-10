
from kivy.core.text import LabelBase
import json
import os

def load_fonts_from_config(config_path="fonts/font_config.json", font_dir="fonts"):
    if not os.path.exists(config_path):
        print("Font config not found.")
        return
    with open(config_path, "r") as f:
        config = json.load(f)
        for entry in config.get("fonts", []):
            name = entry["name"]
            file = entry["file"]
            font_path = os.path.join(font_dir, file)
            if os.path.exists(font_path):
                LabelBase.register(name=name, fn_regular=font_path)
                print(f"Loaded font: {name} from {file}")
            else:
                print(f"Font file not found: {file}")
