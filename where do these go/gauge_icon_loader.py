import os
import json

class GaugeIconLoader:
    def __init__(self, mapping_file="pid_mappings.json"):
        self.mapping_file = mapping_file
        self.pid_icons = {}
        self.load_icons()

    def load_icons(self):
        if os.path.exists(self.mapping_file):
            with open(self.mapping_file, "r") as f:
                data = json.load(f)
                self.pid_icons = {entry["pid"]: entry.get("icon", "") for entry in data}

    def get_icon(self, pid):
        return self.pid_icons.get(pid, "")

    def set_icon(self, pid, icon_filename):
        if os.path.exists(self.mapping_file):
            with open(self.mapping_file, "r") as f:
                data = json.load(f)
            for entry in data:
                if entry["pid"] == pid:
                    entry["icon"] = icon_filename
            with open(self.mapping_file, "w") as f:
                json.dump(data, f, indent=4)
            self.load_icons()
