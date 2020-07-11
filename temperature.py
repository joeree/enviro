from bme280 import BME280 as bme


class Thermometer:
    """ Class to obtain a pressure reading from bme280 and analyze reading """

    def __init__(self, sensor=bme):
        self.sensor = sensor
        self._temperature = None
        self.records = []

    @property
    def temperature(self):  # celsius
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        self._temperature = value

