#include <DHT.h>

// ==================================================
// BatteryMind
// Arduino UNO Sensor Code
// ==================================================


// ==================================================
// PIN DEFINITIONS
// ==================================================

#define VOLTAGE_PIN A0
#define CURRENT_PIN A1
#define DHT_PIN 4

#define DHT_TYPE DHT11


// ==================================================
// DHT SENSOR
// ==================================================

DHT dht(DHT_PIN, DHT_TYPE);


// ==================================================
// ADC SETTINGS
// ==================================================

const float ADC_REF = 5.0;
const int ADC_MAX = 1023;


// ==================================================
// VOLTAGE DIVIDER
// R1 = 30k
// R2 = 7.5k
//
// Battery voltage:
// Arduino pin voltage × (R1 + R2) / R2
// ==================================================

const float R1 = 30000.0;
const float R2 = 7500.0;


// ==================================================
// SETUP
// ==================================================

void setup() {

  Serial.begin(9600);

  dht.begin();

  delay(1000);

  Serial.println("BatteryMind Arduino Started");

}


// ==================================================
// LOOP
// ==================================================

void loop() {


  // ==================================================
  // 1. READ BATTERY VOLTAGE
  // ==================================================

  int voltageRaw = analogRead(VOLTAGE_PIN);

  float voltageAtPin =
    voltageRaw * ADC_REF / ADC_MAX;

  float batteryVoltage =
    voltageAtPin *
    ((R1 + R2) / R2);


  // ==================================================
  // 2. CURRENT
  // ==================================================
  //
  // TEMPORARILY DISABLED
  //
  // ACS712 current measurement is not being used
  // right now.
  //
  // BatteryMind will receive current = 0.0
  //
  // ==================================================

  float current = 0.0;


  // ==================================================
  // 3. READ TEMPERATURE
  // ==================================================

  float temperature =
    dht.readTemperature();


  // ==================================================
  // 4. CHECK TEMPERATURE
  // ==================================================

  if (isnan(temperature)) {

    Serial.println("DHT ERROR");

    delay(1000);

    return;
  }


  // ==================================================
  // 5. SEND JSON
  // ==================================================
  //
  // IMPORTANT:
  // Do NOT print anything else while Python
  // serial_receiver.py is running.
  //
  // Expected format:
  //
  // {
  //   "voltage": 3.850,
  //   "current": 0.000,
  //   "temperature": 29.50
  // }
  //
  // ==================================================

  Serial.print("{\"voltage\":");

  Serial.print(batteryVoltage, 3);

  Serial.print(",\"current\":");

  Serial.print(current, 3);

  Serial.print(",\"temperature\":");

  Serial.print(temperature, 2);

  Serial.println("}");


  // ==================================================
  // 6. ONE SAMPLE EVERY SECOND
  // ==================================================

  delay(1000);

}