# digital_cluster_main.py

import time
import logging
from sensor_manager import SmoothedSensor, CalibrationManager, FilterType, SensorFault
from sensor_ui_config import sensor_ui_config

# Setup logging
logging.basicConfig(filename='gauge_cluster.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Simulated ADC read function placeholder
def read_adc_channel(channel_id):
    # Replace this with actual ADC read logic from the Waveshare ADC
    return 2.5  # Simulated 2.5V read

# Sensor Definitions
sensors = {
    "rpm": SmoothedSensor("RPM", filter_type=FilterType.EXPONENTIAL, alpha=0.2,
                          calibration=CalibrationManager(gain=7000/5.0), display_min=0, display_max=7000),
    "speed": SmoothedSensor("Speed", filter_type=FilterType.EXPONENTIAL, alpha=0.2,
                            calibration=CalibrationManager(gain=120/5.0), display_min=0, display_max=120),
    "coolant_temp": SmoothedSensor("Coolant Temp", filter_type=FilterType.AVERAGE,
                                   calibration=CalibrationManager(custom_fn=lambda v: ((v*100.0)*9/5)+32),
                                   display_min=140, display_max=225),
    "trans_temp": SmoothedSensor("Transmission Temp", filter_type=FilterType.AVERAGE,
                                 calibration=CalibrationManager(custom_fn=lambda v: ((v*100.0)*9/5)+32),
                                 display_min=140, display_max=250),
    "voltage": SmoothedSensor("Voltage", filter_type=FilterType.EXPONENTIAL, alpha=0.15,
                              calibration=CalibrationManager(gain=4.2), display_min=0, display_max=18),
    "oil_pressure": SmoothedSensor("Oil Pressure", filter_type=FilterType.MEDIAN,
                                   calibration=CalibrationManager(custom_fn=lambda v: max(0, (v-0.5)*100)),
                                   display_min=0, display_max=100),
    "fuel_level": SmoothedSensor("Fuel Level", filter_type=FilterType.MEDIAN,
                                 calibration=CalibrationManager(custom_fn=lambda v: max(0, min(100, 100 * ((v - 0.13) / (3.3 - 0.13))))),
                                 display_min=0, display_max=100),
}

# Warning light configuration
warning_conditions = {
    "overheat": lambda s: s["coolant_temp"].get_value() > 220,
    "low_oil": lambda s: s["oil_pressure"].get_value() < 10,
    "low_voltage": lambda s: s["voltage"].get_value() < 11.5,
    "high_trans_temp": lambda s: s["trans_temp"].get_value() > 240,
}

warning_states = {key: False for key in warning_conditions}

def update_warnings():
    for name, condition in warning_conditions.items():
        active = condition(sensors)
        if active != warning_states[name]:
            warning_states[name] = active
            logging.warning(f"Warning light {name} {'ON' if active else 'OFF'}")

def main_loop():
    try:
        while True:
            # Update all sensors
            for name, sensor in sensors.items():
                adc_val = read_adc_channel(name)
                sensor.add_reading(adc_val)
                if sensor.is_faulted():
                    logging.error(f"Sensor {name} fault detected.")

            # Update warning lights
            update_warnings()

            # Print sensor values to terminal for now
            for name, sensor in sensors.items():
                print(f"{name}: {sensor.get_value():.2f} {sensor_ui_config[name]['units']}")

            time.sleep(0.2)  # ~5Hz update rate

    except KeyboardInterrupt:
        print("Shutting down gauge cluster...")

if __name__ == "__main__":
    main_loop()
