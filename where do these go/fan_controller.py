import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import threading
import os

# === CONFIG ===
FAN1_GPIO = 18  # CPU fan
FAN2_GPIO = 13  # Ambient/system fan
DHT_PIN = 4     # AM2302 (DHT22-compatible)

PWM_FREQ = 25000  # Hz
TEMP_INTERVAL = 5  # seconds

# Fan control thresholds (°C)
FAN1_ON_TEMP = 122  # 50°C
FAN1_OFF_TEMP = 113  # 45°C
FAN2_ON_TEMP = 95  # 35°C
FAN2_OFF_TEMP = 86  # 30°C

# === SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN1_GPIO, GPIO.OUT)
GPIO.setup(FAN2_GPIO, GPIO.OUT)

fan1_pwm = GPIO.PWM(FAN1_GPIO, PWM_FREQ)
fan2_pwm = GPIO.PWM(FAN2_GPIO, PWM_FREQ)

fan1_pwm.start(0)
fan2_pwm.start(0)

# === FUNCTIONS ===
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read()) / 1000.0
    except:
        return 0.0

def get_ambient_temp():
    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
    return temp if temp is not None else 0.0

def smooth(current, target, factor=0.1):
    return current + (target - current) * factor

# === CONTROL LOOP ===
def fan_control_loop():
    fan1_speed = 0
    fan2_speed = 0
    fan1_state = False
    fan2_state = False

    while True:
        cpu_temp = get_cpu_temp()
        amb_temp = get_ambient_temp()

        # Hysteresis logic
        fan1_state = fan1_state or cpu_temp >= FAN1_ON_TEMP
        fan1_state = fan1_state and cpu_temp >= FAN1_OFF_TEMP
        fan2_state = fan2_state or amb_temp >= FAN2_ON_TEMP
        fan2_state = fan2_state and amb_temp >= FAN2_OFF_TEMP

        # Map to duty cycle (0–100)
        target1 = min(max((cpu_temp - FAN1_OFF_TEMP) * 20, 0), 100) if fan1_state else 0
        target2 = min(max((amb_temp - FAN2_OFF_TEMP) * 20, 0), 100) if fan2_state else 0

        fan1_speed = smooth(fan1_speed, target1)
        fan2_speed = smooth(fan2_speed, target2)

        fan1_pwm.ChangeDutyCycle(fan1_speed)
        fan2_pwm.ChangeDutyCycle(fan2_speed)

        print(f"[FAN] CPU: {cpu_temp * 9 / 5 + 32:.1f}°F → {fan1_speed:.0f}%, AMB: {amb_temp * 9 / 5 + 32:.1f}°F → {fan2_speed:.0f}%")
        time.sleep(TEMP_INTERVAL)

def start():
    thread = threading.Thread(target=fan_control_loop, daemon=True)
    thread.start()

if __name__ == "__main__":
    try:
        start()
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        fan1_pwm.stop()
        fan2_pwm.stop()
        GPIO.cleanup()
