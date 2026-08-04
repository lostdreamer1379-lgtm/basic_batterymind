"""
=========================================================
BatteryMind Sensor Simulator
=========================================================

Simulates an Arduino UNO sending battery sensor
readings to the Flask backend.

Author:
BatteryMind
"""

import time
import random
import requests

BACKEND_URL = "http://127.0.0.1:5000/battery-data"

print("=" * 60)
print("BatteryMind Sensor Simulator Started")
print("=" * 60)

voltage = 4.20
current = 0.50
temperature = 30.0

cycle = 1

while True:

    ###################################################
    # Simulate Battery Discharge
    ###################################################

    voltage -= random.uniform(0.002, 0.006)

    voltage = max(voltage, 3.20)

    current = random.uniform(0.45, 0.60)

    temperature += random.uniform(-0.05, 0.15)

    ###################################################
    # Create JSON
    ###################################################

    payload = {

        "voltage": round(voltage, 3),

        "current": round(current, 3),

        "temperature": round(temperature, 2)

    }

    ###################################################
    # Send to Backend
    ###################################################

    try:

        response = requests.post(

            BACKEND_URL,

            json=payload,

            timeout=5

        )

        print()

        print("=" * 60)

        print(f"Cycle : {cycle}")

        print("Sent:")

        print(payload)

        print()

        print("Backend Response:")

        print(response.json())

        print("=" * 60)

    except Exception as e:

        print()

        print("Backend not running")

        print(e)

    ###################################################
    # Reset Battery after full discharge
    ###################################################

    if voltage <= 3.20:

        print()

        print("Battery Fully Discharged")

        print("Starting New Charge Cycle")

        print()

        voltage = 4.20

        temperature = 30.0

        cycle += 1

        time.sleep(2)

    ###################################################
    # Sample Rate
    ###################################################

    time.sleep(1)