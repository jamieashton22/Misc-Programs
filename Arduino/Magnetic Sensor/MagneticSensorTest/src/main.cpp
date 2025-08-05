#include <Arduino.h>

// MACROS

#define MAG_SENSOR_PIN A0



// FUNCTION DEFINITIONS

float get_reading(int PinNumber);

// SETUP

void setup() {
 
  pinMode(MAG_SENSOR_PIN, INPUT);

  Serial.begin(9600);
}

// MAIN

void loop() {

  float mag_val = get_reading(MAG_SENSOR_PIN);

  Serial.println(mag_val);

  delay(100);
}

// FUNCTIONS

float get_reading(int PinNumber){

  float mag_val = analogRead(PinNumber);

  return mag_val;

}