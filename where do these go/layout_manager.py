
import json
import os

LAYOUT_DIR = "/home/pi/layout_profiles"
DEFAULT_PROFILE_FILE = "/home/pi/layout_profiles/default_profile.txt"

def ensure_layout_dir():
    if not os.path.exists(LAYOUT_DIR):
        os.makedirs(LAYOUT_DIR)

def save_layout(profile_name, layout):
    ensure_layout_dir()
    path = os.path.join(LAYOUT_DIR, f"{profile_name}.json")
    with open(path, "w") as f:
        json.dump(layout, f)

def load_layout(profile_name):
    path = os.path.join(LAYOUT_DIR, f"{profile_name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def list_profiles():
    ensure_layout_dir()
    return [f.replace(".json", "") for f in os.listdir(LAYOUT_DIR) if f.endswith(".json")]

def set_default_profile(profile_name):
    ensure_layout_dir()
    with open(DEFAULT_PROFILE_FILE, "w") as f:
        f.write(profile_name)

def get_default_profile():
    if os.path.exists(DEFAULT_PROFILE_FILE):
        with open(DEFAULT_PROFILE_FILE, "r") as f:
            return f.read().strip()
    return None

def get_last_used_profile():
    return get_default_profile()


def extract_dynamic_gauges(self, gauge_screen):
    return [
        {
            "name": g.label,
            "unit": g.unit,
            "gauge_type": g.gauge_type,
            "min_val": g.min_val,
            "max_val": g.max_val,
            "pos_hint": g.pos_hint,
            "size_hint": g.size_hint,
        }
        for g in getattr(gauge_screen, "gauges", [])
    ]

def apply_dynamic_gauges(self, gauge_screen, gauge_list):
    for g in gauge_list:
        from draggable_gauge import DraggableGauge
        new_gauge = DraggableGauge(
            label=g["name"],
            unit=g["unit"],
            gauge_type=g["gauge_type"],
            min_val=g["min_val"],
            max_val=g["max_val"],
            pos_hint=g["pos_hint"],
            size_hint=g["size_hint"],
        )
        gauge_screen.add_widget(new_gauge)
        gauge_screen.gauges.append(new_gauge)
