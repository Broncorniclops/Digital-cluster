import RPi.GPIO as GPIO
import time
import os
import logging
import socket

# === CONFIG ===
SHUTDOWN_PIN = 26  # GPIO pin from UPS HAT that indicates power loss
ACC_PIN = 5        # GPIO pin for ACC (ignition) signal
SHUTDOWN_DELAY_ACC_OFF = 15  # seconds
BATTERY_SHUTDOWN_VOLTAGE = 3.2  # volts
LOG_FILE = "/var/log/ups_monitor.log"

# === Setup Logging ===
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def notify_ui(message):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect("/tmp/shutdown_ui.sock")
            s.sendall(message.encode())
    except Exception as e:
        logging.error("Failed to notify UI: %s", e)

def get_battery_voltage():
    try:
        import smbus2
        bus = smbus2.SMBus(1)
        raw = bus.read_word_data(0x36, 0x02)
        swapped = ((raw & 0xFF) << 8) | (raw >> 8)
        voltage = (swapped >> 4) * 1.25 / 1000
        return round(voltage, 2)
    except Exception as e:
        logging.error("Failed to read battery voltage: %s", e)
        return 0.0

def shutdown(reason):
    logging.warning("Shutdown initiated: %s", reason)
    os.system("sudo shutdown -h now")

def monitor_loop():
    logging.info("UPS Monitor Started.")
    while True:
        if GPIO.input(SHUTDOWN_PIN) == GPIO.HIGH:
            acc_state = GPIO.input(ACC_PIN)
            if acc_state == GPIO.HIGH:
                logging.info("Power loss detected, but ACC is still ON. Monitoring battery voltage...")
                notify_ui("shutdown_pending")
                while True:
                    voltage = get_battery_voltage()
                    logging.info("Battery Voltage: %.2fV", voltage)
                    if GPIO.input(SHUTDOWN_PIN) == GPIO.LOW:
                        logging.info("Power restored. Aborting shutdown.")
                        notify_ui("shutdown_clear")
                        break
                    if voltage < BATTERY_SHUTDOWN_VOLTAGE:
                        shutdown("UPS battery voltage low (%.2fV)" % voltage)
                        return
                    time.sleep(10)
            else:
                logging.info("Power loss detected and ACC is OFF. Shutting down in %d seconds...", SHUTDOWN_DELAY_ACC_OFF)
                notify_ui("shutdown_pending")
                time.sleep(SHUTDOWN_DELAY_ACC_OFF)
                if GPIO.input(SHUTDOWN_PIN) == GPIO.HIGH:
                    shutdown("ACC off and power lost.")
                else:
                    logging.info("Power restored during delay. Shutdown canceled.")
                    notify_ui("shutdown_clear")
        time.sleep(2)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ACC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logging.info("UPS monitor stopped by user.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
