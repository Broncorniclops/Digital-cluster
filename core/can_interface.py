
import json
import os

PID_MAP_FILE = "pid_map.json"
pid_map = {}

def load_pid_map():
    global pid_map
    if os.path.exists(PID_MAP_FILE):
        with open(PID_MAP_FILE, "r") as f:
            pid_map = json.load(f)

load_pid_map()

def apply_custom_pid(pid, raw_value):
    pid_hex = hex(pid)
    if pid_hex in pid_map:
        try:
            x = raw_value
            result = eval(pid_map[pid_hex]["formula"])
            label = pid_map[pid_hex].get("label", pid_hex)
            unit = pid_map[pid_hex].get("unit", "")
            return {"label": label, "value": result, "unit": unit, "pid": pid_hex}
        except Exception as e:
            return {"label": pid_hex, "value": raw_value, "unit": "", "pid": pid_hex, "error": str(e)}
    return None

import can
import threading

class CANInput:
    def __init__(self, channel='can0', bitrate=500000):
        self.bus = can.interface.Bus(channel=channel, bustype='socketcan')
        self.listeners = {}
        self.data = {}
        self.running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def register(self, msg_id, callback):
        self.listeners[msg_id] = callback

    def listen(self):
        while self.running:
            msg = self.bus.recv()
            if msg and msg.arbitration_id in self.listeners:
                self.listeners[msg.arbitration_id](msg)

    def stop(self):
        self.running = False
        self.thread.join()

# Shared data dictionary
CAN_DATA = {
    "rpm": 0.0,
    "speed": 0.0,
    "coolant_temp": 0.0,
    "trans_temp": 0.0,
    "voltage": 0.0
}

# Decoders
def decode_rpm(msg):
    rpm_raw = (msg.data[3] << 8) | msg.data[2]
    CAN_DATA['rpm'] = rpm_raw * 0.125

def decode_speed(msg):
    CAN_DATA['speed'] = msg.data[1]

def decode_coolant_temp(msg):
    CAN_DATA['coolant_temp'] = msg.data[0] - 40

def decode_trans_temp(msg):
    raw = msg.data[2]
    CAN_DATA['trans_temp'] = raw - 40

def decode_voltage(msg):
    raw = (msg.data[0] << 8) | msg.data[1]
    CAN_DATA['voltage'] = raw * 0.001  # Assume 1mV/bit, example scaling

def init_can():
    can_reader = CANInput()
    can_reader.register(0x0CFF0500, decode_rpm)
    can_reader.register(0x18FEF100, decode_speed)
    can_reader.register(0x18FEEE00, decode_coolant_temp)
    can_reader.register(0x18FEF200, decode_trans_temp)  # Example ID
    can_reader.register(0x18FEBB00, decode_voltage)     # Example ID
    return can_reader
