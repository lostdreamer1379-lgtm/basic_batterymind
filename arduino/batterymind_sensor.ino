/*
================================================

BatteryMind
Explainable AI-driven IoT Battery Health System

Arduino Sensor Node

Hardware:

Arduino UNO

Sensors:
- Voltage Divider
- ACS712 Current Sensor
- DHT11/DHT22 Temperature Sensor
- Pause Button


Output JSON:

{
"voltage":3.82,
"current":0.45,
"temperature":31.5
}

================================================
*/


#include <Arduino.h>
#include <DHT.h>


// ===============================
// Pin Configuration
// ===============================


#define VOLTAGE_PIN A0

#define CURRENT_PIN A1


#define DHT_PIN 2

#define BUTTON_PIN 3



// DHT Type

#define DHTTYPE DHT11
// Change to DHT22 if using DHT22



DHT dht(
  DHT_PIN,
  DHTTYPE
);



// ===============================
// Voltage Sensor Parameters
// ===============================


// Voltage divider values

// Example:
// R1 = 30k
// R2 = 7.5k

float R1 = 30000.0;

float R2 = 7500.0;



float voltageCalibration = 1.0;




// ===============================
// ACS712 Parameters
// ===============================


// ACS712 sensitivity

// 5A  = 185 mV/A
// 20A = 100 mV/A
// 30A = 66 mV/A


float sensitivity = 0.185;



// ACS712 zero current voltage

float zeroCurrentVoltage = 2.5;



// ===============================
// Button Variables
// ===============================


bool paused = false;


bool lastButtonState = HIGH;



unsigned long lastDebounceTime = 0;


unsigned long debounceDelay = 200;



// ===============================
// Timing
// ===============================


unsigned long previousMillis = 0;


unsigned long interval = 1000;



// =================================================
// SETUP
// =================================================


void setup()
{


Serial.begin(9600);



dht.begin();



pinMode(
BUTTON_PIN,
INPUT_PULLUP
);



Serial.println(
"BatteryMind Sensor Started"
);


}




// =================================================
// Read Battery Voltage
// =================================================


float readVoltage()
{


int adcValue =
analogRead(
VOLTAGe_PIN
);



float adcVoltage =
(adcValue * 5.0)
/
1023.0;



// Voltage divider calculation


float batteryVoltage =
adcVoltage *
(
(R1 + R2)
/
R2
);



batteryVoltage *=
voltageCalibration;



return batteryVoltage;



}



// =================================================
// Read Current Using ACS712
// =================================================


float readCurrent()
{


int adcValue =
analogRead(
CURRENT_PIN
);



float sensorVoltage =
(adcValue * 5.0)
/
1023.0;



float current =
(
sensorVoltage -
zeroCurrentVoltage
)
/
sensitivity;



return current;



}



// =================================================
// Read Temperature
// =================================================


float readTemperature()
{


float temp =
dht.readTemperature();



if(
isnan(temp)
)
{

return 0;

}



return temp;



}



// =================================================
// Button Handling
// =================================================


void checkPauseButton()
{


bool buttonState =
digitalRead(
BUTTON_PIN
);



if(
buttonState == LOW &&
lastButtonState == HIGH
)

{


if(
millis()
-
lastDebounceTime
>
debounceDelay
)

{

paused =
!paused;


lastDebounceTime =
millis();


}

}



lastButtonState =
buttonState;



}



// =================================================
// Send JSON Data
// =================================================


void sendBatteryData()
{


float voltage =
readVoltage();



float current =
readCurrent();



float temperature =
readTemperature();



Serial.print("{");



Serial.print("\"voltage\":");

Serial.print(
voltage,
2
);



Serial.print(",");



Serial.print("\"current\":");

Serial.print(
current,
2
);



Serial.print(",");



Serial.print("\"temperature\":");

Serial.print(
temperature,
2
);



Serial.println("}");



}



// =================================================
// MAIN LOOP
// =================================================


void loop()
{


checkPauseButton();



if(
paused
)

{


return;


}



unsigned long currentMillis =
millis();



if(
currentMillis -
previousMillis
>= interval
)

{


previousMillis =
currentMillis;



sendBatteryData();



}



}