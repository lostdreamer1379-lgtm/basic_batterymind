"""
=========================================================
BatteryMind Feature Engineering Engine
=========================================================

Converts raw IoT sensor readings into the
28 engineered features required by the
BatteryMind Random Forest model.

Author:
BatteryMind
"""

import numpy as np
import pandas as pd

from collections import deque
from datetime import datetime


class BatteryFeatureEngine:

    def __init__(self, window_size=100):

        self.window_size = window_size

        # Rolling buffers

        self.voltage_buffer = deque(maxlen=window_size)
        self.current_buffer = deque(maxlen=window_size)
        self.temperature_buffer = deque(maxlen=window_size)
        self.timestamp_buffer = deque(maxlen=window_size)

    ###########################################################
    # Buffer Management
    ###########################################################

    def add_reading(self, voltage, current, temperature):

        self.voltage_buffer.append(float(voltage))
        self.current_buffer.append(float(current))
        self.temperature_buffer.append(float(temperature))

        self.timestamp_buffer.append(datetime.now())

    def reset(self):

        self.voltage_buffer.clear()
        self.current_buffer.clear()
        self.temperature_buffer.clear()
        self.timestamp_buffer.clear()

    def size(self):

        return len(self.voltage_buffer)

    def is_ready(self):

        return len(self.voltage_buffer) >= self.window_size

    ###########################################################
    # Internal Helpers
    ###########################################################

    def _voltage(self):

        return np.array(self.voltage_buffer)

    def _current(self):

        return np.array(self.current_buffer)

    def _temperature(self):

        return np.array(self.temperature_buffer)

    ###########################################################
    # Time
    ###########################################################

    def get_time_duration(self):

        if len(self.timestamp_buffer) < 2:
            return 0.0

        start = self.timestamp_buffer[0]
        end = self.timestamp_buffer[-1]

        return (end - start).total_seconds()

    def get_sample_count(self):

        return len(self.voltage_buffer)

    ###########################################################
    # Statistical Functions
    ###########################################################

    def _mean(self, data):

        return float(np.mean(data))

    def _max(self, data):

        return float(np.max(data))

    def _min(self, data):

        return float(np.min(data))

    def _std(self, data):

        return float(np.std(data))

    def _median(self, data):

        return float(np.median(data))

    def _rms(self, data):

        return float(np.sqrt(np.mean(np.square(data))))

    def _range(self, data):

        return float(np.max(data) - np.min(data))

    ###########################################################
    # Time Array
    ###########################################################

    def get_time_array(self):

        """
        Creates elapsed time array from timestamps.

        This is closer to the NASA dataset than simply
        assuming every sample is equally spaced.
        """

        if len(self.timestamp_buffer) == 0:
            return np.array([])

        first = self.timestamp_buffer[0]

        elapsed = []

        for t in self.timestamp_buffer:

            elapsed.append(
                (t - first).total_seconds()
            )

        return np.array(elapsed)
        ###########################################################
    # Energy
    ###########################################################

    def calculate_energy(self):

        """
        Energy = ∫ V × |I| dt
        Matches the training notebook.
        """

        voltage = self._voltage()
        current = self._current()
        time = self.get_time_array()

        if len(voltage) < 2:
            return 0.0

        if len(time) != len(voltage):
            return 0.0

        energy = np.trapz(
            voltage * np.abs(current),
            time
        )

        return float(energy)

    ###########################################################
    # Average Power
    ###########################################################

    def calculate_average_power(self):

        duration = self.get_time_duration()

        if duration <= 0:
            return 0.0

        energy = self.calculate_energy()

        return float(energy / duration)

    ###########################################################
    # Voltage Drop Rate
    ###########################################################

    def calculate_voltage_drop_rate(self):

        voltage = self._voltage()

        duration = self.get_time_duration()

        if len(voltage) < 2:
            return 0.0

        if duration <= 0:
            return 0.0

        return float(
            (voltage[0] - voltage[-1]) / duration
        )

    ###########################################################
    # Temperature Rise
    ###########################################################

    def calculate_temperature_rise(self):

        temperature = self._temperature()

        if len(temperature) < 2:
            return 0.0

        return float(
            temperature[-1] - temperature[0]
        )

    ###########################################################
    # Current Stability
    ###########################################################

    def calculate_current_stability(self):

        current = self._current()

        if len(current) == 0:
            return 0.0

        return float(np.std(current))

    ###########################################################
    # Voltage Feature Dictionary
    ###########################################################

    def voltage_features(self):

        voltage = self._voltage()

        return {
            "Voltage_mean": self._mean(voltage),
            "Voltage_max": self._max(voltage),
            "Voltage_min": self._min(voltage),
            "Voltage_std": self._std(voltage),
            "Voltage_median": self._median(voltage),
            "Voltage_rms": self._rms(voltage),
            "Voltage_range": self._range(voltage)
        }

    ###########################################################
    # Current Feature Dictionary
    ###########################################################

    def current_features(self):

        current = self._current()

        return {
            "Current_mean": self._mean(current),
            "Current_max": self._max(current),
            "Current_min": self._min(current),
            "Current_std": self._std(current),
            "Current_median": self._median(current),
            "Current_rms": self._rms(current),
            "Current_range": self._range(current)
        }

    ###########################################################
    # Temperature Feature Dictionary
    ###########################################################

    def temperature_features(self):

        temperature = self._temperature()

        return {
            "Temperature_mean": self._mean(temperature),
            "Temperature_max": self._max(temperature),
            "Temperature_min": self._min(temperature),
            "Temperature_std": self._std(temperature),
            "Temperature_median": self._median(temperature),
            "Temperature_rms": self._rms(temperature),
            "Temperature_range": self._range(temperature)
        }
        ###########################################################
    # Extract All Features
    ###########################################################

    def extract_features(self):

        """
        Returns all 28 features in the exact order
        expected by the BatteryMind ML model.
        """

        if not self.is_ready():

            raise ValueError(
                f"Need {self.window_size} samples. "
                f"Current samples: {self.size()}"
            )

        features = {}

        #######################################################
        # Voltage
        #######################################################

        features.update(
            self.voltage_features()
        )

        #######################################################
        # Current
        #######################################################

        features.update(
            self.current_features()
        )

        #######################################################
        # Temperature
        #######################################################

        features.update(
            self.temperature_features()
        )

        #######################################################
        # Time
        #######################################################

        features["Time_duration"] = self.get_time_duration()

        features["Time_samples"] = self.get_sample_count()

        #######################################################
        # Energy
        #######################################################

        features["Energy"] = self.calculate_energy()

        features["Average_Power"] = self.calculate_average_power()

        #######################################################
        # Battery Degradation Features
        #######################################################

        features["Voltage_Drop_Rate"] = \
            self.calculate_voltage_drop_rate()

        features["Temperature_Rise"] = \
            self.calculate_temperature_rise()

        features["Current_Stability"] = \
            self.calculate_current_stability()

        return features

    ###########################################################
    # Convert to DataFrame
    ###########################################################

    def to_dataframe(self):

        return pd.DataFrame(
            [self.extract_features()]
        )
###############################################################
# Testing
###############################################################

if __name__ == "__main__":

    engine = BatteryFeatureEngine(
        window_size=100
    )

    print("=" * 60)
    print("BatteryMind Feature Engine Test")
    print("=" * 60)

    for i in range(100):

        voltage = 4.20 - (i * 0.003)

        current = 0.50 + np.random.normal(
            0,
            0.02
        )

        temperature = 30 + (i * 0.04)

        engine.add_reading(
            voltage,
            current,
            temperature
        )

    print()

    print("Buffer Ready :", engine.is_ready())
    print("Samples      :", engine.size())

    print()

    df = engine.to_dataframe()

    print(df.T)

    print()

    print("=" * 60)
    print("Feature Count :", len(df.columns))
    print("=" * 60)
