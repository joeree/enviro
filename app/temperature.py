from bme280 import BME280 as bme
from smbus import SMBus

class Thermometer:
    """ Class to obtain a pressure reading from bme280 and analyze reading """

    def __init__(self, sensor=bme, bus=SMBus):
        self.bus = bus(1)
        self.sensor = sensor(i2c_dev=self.bus)
        self._temperature = None
        self.records = []

    @property
    def temperature(self):  # celsius
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        self._temperature = value

    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp
