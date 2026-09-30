"""
==================================================

BatteryMind
Arduino Serial Communication Bridge

Reads JSON from Arduino UNO
resets the Flask feature buffer on startup
and forwards sensor data to Flask backend.

==================================================
"""

import serial
import requests
import json
from datetime import datetime


# ==================================================
# SETTINGS
# ==================================================

SERIAL_PORT = "COM4"  # Update this to your Arduino's serial port
BAUD_RATE = 9600

FLASK_BASE_URL = "http://127.0.0.1:5000"

DATA_URL = f"{FLASK_BASE_URL}/battery-data"
RESET_URL = f"{FLASK_BASE_URL}/reset"


# ==================================================
# CONNECT TO ARDUINO
# ==================================================

try:

    arduino = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    print("=" * 60)
    print("BatteryMind Serial Receiver")
    print("=" * 60)
    print("Arduino Connected")

except Exception as e:

    print("Serial Error:", e)
    exit()


# ==================================================
# RESET BACKEND BUFFER
# ==================================================

def reset_backend():

    try:

        response = requests.post(
            RESET_URL,
            json={
                "window_size": 300
            },
            timeout=5
        )

        response.raise_for_status()

        result = response.json()

        print("Backend Buffer Reset")
        print("Window Size:", result.get("window_size"))
        print("=" * 60)

        return True

    except Exception as e:

        print("Backend Reset Error:", e)
        return False


# ==================================================
# SEND DATA TO BACKEND
# ==================================================

def send_to_backend(data):

    try:

        # Add timestamp
        data["timestamp"] = datetime.now().isoformat()

        response = requests.post(
            DATA_URL,
            json=data,
            timeout=5
        )

        result = response.json()

        # ------------------------------------------
        # BUFFER STILL COLLECTING
        # ------------------------------------------

        if result.get("status") == "Collecting":

            print(
                f"Sample "
                f"{result.get('samples')}/"
                f"{result.get('required')}"
            )

        # ------------------------------------------
        # MODEL READY
        # ------------------------------------------

        elif result.get("status") == "success":

            prediction = result.get(
                "prediction",
                {}
            )

            print(
                f"Sample complete | "
                f"SOH: {prediction.get('soh')} | "
                f"Health: {prediction.get('health')} | "
                f"Risk: {prediction.get('risk')}"
            )

        # ------------------------------------------
        # BACKEND ERROR
        # ------------------------------------------

        elif result.get("status") == "error":

            print(
                "Backend Error:",
                result.get("message")
            )

        else:

            print("Backend:", result)

    except requests.exceptions.ConnectionError:

        print(
            "Backend connection failed. "
            "Is Flask running?"
        )

    except Exception as e:

        print("Backend Error:", e)


# ==================================================
# RESET BEFORE STARTING DATA COLLECTION
# ==================================================

if not reset_backend():

    print(
        "\nWARNING: Backend could not be reset."
    )

    print(
        "Make sure Flask is running before "
        "starting the receiver."
    )

    arduino.close()

    exit()


print("Starting sensor data collection...")
print("Samples: 0/300")
print("=" * 60)


# ==================================================
# MAIN LOOP
# ==================================================

try:

    while True:

        line = (
            arduino.readline()
            .decode(
                "utf-8",
                errors="ignore"
            )
            .strip()
        )

        if not line:
            continue


        # ------------------------------------------
        # PARSE ARDUINO JSON
        # ------------------------------------------

        try:

            data = json.loads(line)

        except json.JSONDecodeError:

            print(
                "Invalid Arduino JSON:",
                line
            )

            continue


        # ------------------------------------------
        # VALIDATE SENSOR DATA
        # ------------------------------------------

        required_fields = [
            "voltage",
            "current",
            "temperature"
        ]

        if not all(
            field in data
            for field in required_fields
        ):

            print(
                "Invalid sensor data:",
                data
            )

            continue


        # ------------------------------------------
        # DISPLAY SENSOR DATA
        # ------------------------------------------

        print(
            f"Arduino → "
            f"V={data['voltage']} V | "
            f"I={data['current']} A | "
            f"T={data['temperature']} °C"
        )


        # ------------------------------------------
        # SEND TO FLASK
        # ------------------------------------------

        send_to_backend(data)


# ==================================================
# STOP
# ==================================================

except KeyboardInterrupt:

    print("\n")
    print("=" * 60)
    print("Serial Receiver Stopped")
    print("=" * 60)


finally:

    arduino.close()