import config_manager
import random

try:
    from can_interface import CAN_DATA, init_can
    CAN_ENABLED = True
    can_reader = init_can()
except ImportError:
    CAN_DATA = {}
    CAN_ENABLED = False

try:
    from ups_i2c_reader import UPS_DATA, start_polling as start_ups_polling
    UPS_ENABLED = True
    start_ups_polling()
except ImportError:
    UPS_DATA = {}
    UPS_ENABLED = False

class Sensor:
    def __init__(self, name, min_val, max_val, unit, smoothing="exp", redline=None, converter=None, can_key=None, ups_key=None):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.unit = unit
        self.redline = redline
        self.converter = converter
        self.can_key = can_key
        self.ups_key = ups_key
        self.value = 0
        self.filtered = 0
        self.fault = False
        self.message = ""
        self.alpha = 0.2

    def read_raw(self):
        if self.can_key and self.can_key in CAN_DATA:
            return CAN_DATA[self.can_key]
        if self.ups_key and self.ups_key in UPS_DATA:
            return UPS_DATA[self.ups_key]
        return random.uniform(self.min_val - 10, self.max_val + 10)

    def apply_filter(self, raw):
        if self.filtered == 0:
            self.filtered = raw
        else:
            self.filtered = self.alpha * raw + (1 - self.alpha) * self.filtered
        return self.filtered

    def check_faults(self, raw):
        if raw < self.min_val or raw > self.max_val:
            self.fault = True
            self.message = f"{self.name} out of range"
        else:
            self.fault = False
            self.message = ""

    def convert_units(self, raw):
        return self.converter(raw) if self.converter else raw

    def update(self):
        raw = self.read_raw()
        self.check_faults(raw)
        filtered = self.apply_filter(raw)
        self.value = self.convert_units(filtered)

    def get_status(self):
        return {
            "value": round(self.value, 1),
            "fault": self.fault,
            "message": self.message
        }

# Conversion examples
def voltage_to_psi(v): return v * 25
def voltage_to_temp_f(v): return v * 20 + 100
def resistance_to_percent(v): return min(100, max(0, (v - 15) / (160 - 15) * 100))

# Sensor list
sensors = {
    "rpm": Sensor("RPM", 0, 7000, "rpm", can_key="rpm"),
    "speed": Sensor("Speed", 0, 120, "mph", can_key="speed"),
    "coolant_temp": Sensor("Coolant Temp", 140, 225, "°F", converter=voltage_to_temp_f, can_key="coolant_temp"),
    "trans_temp": Sensor("Trans Temp", 140, 250, "°F", converter=voltage_to_temp_f, can_key="trans_temp"),
    "oil_pressure": Sensor("Oil Pressure", 0, 100, "psi", converter=voltage_to_psi),
    "voltage": Sensor("Voltage", 10, 15, "V", can_key="voltage"),
    "fuel_level": Sensor("Fuel", 0, 100, "%", converter=resistance_to_percent),
    "afr": Sensor("AFR", 10, 17, "AFR", can_key="afr"),
    "ups_batt": Sensor("UPS Battery", 2.5, 4.2, "V", ups_key="voltage")
}

def read_all():
    for s in sensors.values():
        s.update()
    return {name: s.get_status() for name, s in sensors.items()}
