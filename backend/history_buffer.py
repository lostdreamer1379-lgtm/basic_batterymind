"""
======================================================
BatteryMind
History Buffer

Stores the latest sensor readings.

The feature engineering engine uses this history
instead of a single sensor reading.

======================================================
"""

from collections import deque


# Number of samples kept in memory
WINDOW_SIZE = 60


class BatteryHistory:

    def __init__(self):

        self.voltage = deque(maxlen=WINDOW_SIZE)
        self.current = deque(maxlen=WINDOW_SIZE)
        self.temperature = deque(maxlen=WINDOW_SIZE)

    def add(self, voltage, current, temperature):

        self.voltage.append(float(voltage))
        self.current.append(float(current))
        self.temperature.append(float(temperature))

    def ready(self):
        """
        Returns True once enough samples
        have been collected.
        """
        return len(self.voltage) >= WINDOW_SIZE

    def get_voltage(self):
        return list(self.voltage)

    def get_current(self):
        return list(self.current)

    def get_temperature(self):
        return list(self.temperature)

    def size(self):
        return len(self.voltage)

    def clear(self):

        self.voltage.clear()
        self.current.clear()
        self.temperature.clear()


# Global history object
battery_history = BatteryHistory()