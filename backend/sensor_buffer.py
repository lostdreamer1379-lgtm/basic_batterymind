"""
=========================================
BatteryMind
Sensor Buffer

Stores the latest sensor readings
for feature extraction.

=========================================
"""

from collections import deque


# Number of samples used to compute features
WINDOW_SIZE = 60


# Buffers
voltage_buffer = deque(maxlen=WINDOW_SIZE)
current_buffer = deque(maxlen=WINDOW_SIZE)
temperature_buffer = deque(maxlen=WINDOW_SIZE)


def add_reading(voltage, current, temperature):
    """
    Add a new sensor reading.
    """

    voltage_buffer.append(float(voltage))
    current_buffer.append(float(current))
    temperature_buffer.append(float(temperature))


def is_ready():
    """
    Returns True once enough samples
    have been collected.
    """

    return len(voltage_buffer) == WINDOW_SIZE


def get_buffers():
    """
    Returns all sensor histories.
    """

    return (
        list(voltage_buffer),
        list(current_buffer),
        list(temperature_buffer)
    )


def clear_buffers():
    """
    Clears all stored samples.
    """

    voltage_buffer.clear()
    current_buffer.clear()
    temperature_buffer.clear()


def sample_count():
    """
    Returns current number of samples.
    """

    return len(voltage_buffer)