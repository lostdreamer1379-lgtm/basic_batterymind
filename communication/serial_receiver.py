"""
==================================================

BatteryMind

Arduino Serial Communication Bridge


Reads JSON from Arduino UNO

and forwards it to Flask backend.


==================================================
"""


import serial
import requests
import json
import time



# ==========================
# SETTINGS
# ==========================


SERIAL_PORT = "COM3"


BAUD_RATE = 9600



FLASK_URL = (

"http://127.0.0.1:5000/battery-data"

)





# ==========================
# CONNECT SERIAL
# ==========================


try:


    arduino = serial.Serial(

        SERIAL_PORT,

        BAUD_RATE,

        timeout=1

    )


    print(
        "Arduino Connected"
    )


except Exception as e:


    print(
        "Serial Error:",
        e
    )

    exit()





# ==========================
# DATA FORWARDING
# ==========================


def send_to_backend(data):


    try:


        response=requests.post(

            FLASK_URL,

            json=data

        )


        print(

            "Backend:",

            response.json()

        )



    except Exception as e:


        print(
            "Backend Error:",
            e
        )






# ==========================
# MAIN LOOP
# ==========================


while True:


    try:


        line = (

            arduino.readline()

            .decode()

            .strip()

        )



        if line:


            print(

                "Arduino:",

                line

            )



            try:


                data=json.loads(
                    line
                )



                send_to_backend(
                    data
                )



            except json.JSONDecodeError:


                print(
                    "Invalid JSON"
                )




    except KeyboardInterrupt:


        print(
            "Stopping..."
        )

        break



    except Exception as e:


        print(
            e
        )

