import smbus2
import time
import threading
import logging

I2C_ADDR = 0x36  # Replace with actual UPS I2C address if different
BUS_NUM = 1
LOG_FILE = "/var/log/ups_data.log"

UPS_DATA = {
    "voltage": 0.0,
    "percent": 0,
    "low_voltage": False,
    "message": ""
}

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def estimate_battery_percent(voltage):
    # Simple linear estimate between 2.5V (0%) and 4.2V (100%)
    return max(0, min(100, int((voltage - 2.5) / (4.2 - 2.5) * 100)))

def read_voltage():
    try:
        bus = smbus2.SMBus(BUS_NUM)
        raw = bus.read_word_data(I2C_ADDR, 0x02)
        raw_swapped = ((raw & 0xFF) << 8) | (raw >> 8)
        voltage = (raw_swapped >> 4) * 1.25 / 1000
        percent = estimate_battery_percent(voltage)

        UPS_DATA["voltage"] = round(voltage, 2)
        UPS_DATA["percent"] = percent
        UPS_DATA["low_voltage"] = voltage < 3.2
        UPS_DATA["message"] = "LOW BATTERY" if UPS_DATA["low_voltage"] else ""

        return voltage, percent
    except Exception as e:
        UPS_DATA["voltage"] = 0.0
        UPS_DATA["percent"] = 0
        UPS_DATA["low_voltage"] = True
        UPS_DATA["message"] = "ERROR"

def start_polling(interval=10.0, log_interval=300):
    def loop():
        counter = 0
        while True:
            result = read_voltage()
            counter += interval
            if result and counter >= log_interval:
                voltage, percent = result
                logging.info(f"UPS Voltage: {voltage:.2f}V, Battery: {percent}%")
                counter = 0
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
