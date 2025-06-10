import board
import busio
import adafruit_tsl2591

class AmbientLightSensor:
    def __init__(self, alpha=0.2):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_tsl2591.TSL2591(i2c)
        self.alpha = alpha  # smoothing factor
        self.smoothed_lux = None

    def read_lux(self):
        raw_lux = self.sensor.lux or 0.0
        if self.smoothed_lux is None:
            self.smoothed_lux = raw_lux
        else:
            self.smoothed_lux = (self.alpha * raw_lux) + ((1 - self.alpha) * self.smoothed_lux)
        return round(self.smoothed_lux, 2)

    def is_dark(self, threshold=20):
        return self.read_lux() < threshold