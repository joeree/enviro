import time
from bme280 import BME280 as bme
from smbus import SMBus


class Barometer:
    """ Class to obtain a pressure reading from bme280 and analyze reading """

    ALTITUDE_OFFSET = 30
    RECORDS_LENGTH = 1000

    def __init__(self, sensor=bme, bus=SMBus):
        self.bus = bus(1)
        self.sensor = sensor(ic2_dev=self.bus)
        self._pressure = None
        self._pressure_reading = None
        self.records = []

    @property
    def pressure(self):  # hPa float
        return self._pressure

    @pressure.setter
    def pressure(self, value: float):
        self._pressure = value

    @property
    def pressure_reading(self):  # human-readable string
        return self._pressure_reading

    @pressure_reading.setter
    def pressure_reading(self, value: str):
        self._pressure_reading = value

    def get_pressure(self):
        """ Take pressure reading and record if different than previous reading """
        self.pressure = self.sensor.get_pressure() + self.ALTITUDE_OFFSET
        if self.records and self.records[-1][0] == self.pressure:
            return
        self.records.append((self.pressure, time.time()))
        if len(self.records) > self.RECORDS_LENGTH:
            self.records.pop(0)

    def analyze_pressure(self) -> str:
        """ Analyzes pressure reading according to traditional methods
        Returns:
            reading: Human read-able interpretation of the pressure reading
        """
        if self.pressure > 1022.689:  # high pressure
            reading = 'high'
            """
            Rising or steady pressure means continued fair weather.
            Slowly falling pressure means fair weather
            Rapidly falling pressure means cloudy and warmer conditions
            """
        elif self.pressure < 1009.144:  # low pressure
            reading = 'low'
            """
            Rising or steady pressure means present conditions will continue
            Slowly falling pressure means little change in the weather
            Rapidly falling pressure means that precipitation is likely
            """
        else:  # average pressure
            reading = 'normal'
            """
            rising or steady pressure indicates clearing & cooler weather
            slowly falling pressure indicates rain
            rapidly falling pressure indicates a storm is coming
            """
        return reading

    def calculate_slope(self, measure_1: tuple, measure_2: tuple) -> float:
        """ Calculates the slope of the pressure change over time to determine severity of change
        Attr:
            measure_1 & measure_2: tuples containing a pressure reading (hPa) and timestamp
        Returns:
            slope
        """
        slope = (measure_2[0]-measure_1[0])/(measure_2[1]-measure_1[1])
        return slope
