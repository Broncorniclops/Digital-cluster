
import can
import time
import logging

from config_manager import config_manager

bus = can.interface.Bus(channel='can0', bustype='socketcan')

def get_dtc_list():
    dtcs = []
    try:
        msg = can.Message(arbitration_id=0x7DF,
                          data=[0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          is_extended_id=False)
        bus.send(msg)
        time.sleep(0.2)
        for _ in range(10):
            response = bus.recv(0.1)
            if response and response.arbitration_id in range(0x7E8, 0x7EF):
                dtcs += parse_dtc_response(response.data)
    except Exception as e:
        logging.error(f"DTC read error: {e}")
    return dtcs

def clear_dtc():
    try:
        msg = can.Message(arbitration_id=0x7DF,
                          data=[0x04, 0x14, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                          is_extended_id=False)
        bus.send(msg)
    except Exception as e:
        logging.error(f"DTC clear error: {e}")

def parse_dtc_response(data):
    dtcs = []
    if len(data) < 3 or data[0] < 0x03:
        return dtcs
    count = (len(data) - 2) // 2
    for i in range(count):
        b1 = data[2 + i * 2]
        b2 = data[3 + i * 2]
        code_type = (b1 & 0xC0) >> 6
        letter = "PBCU"[code_type]
        code = f"{letter}{(b1 & 0x3F):02X}{b2:02X}"
        dtcs.append((code, decode_dtc(code)))
    return dtcs

def decode_dtc(code):
    if code.startswith("P03"):
        return "Engine Misfire"
    if code == "P0420":
        return "Catalyst Efficiency Below Threshold"
    return "Unknown DTC"
