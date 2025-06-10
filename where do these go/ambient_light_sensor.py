import board
import busio
import adafruit_tsl2591

class AmbientLightSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_tsl2591.TSL2591(i2c)

    def read_lux(self):
        return self.sensor.lux

    def is_dark(self, threshold=20):
        lux = self.read_lux()
        return lux < threshold
