#include <Arduino.h>

#define TRIG 5
#define ECHO 6

float duration, distance;

float get_distance(float _duration);

void setup() {

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.begin(9600);

}

void loop() {

  digitalWrite(TRIG, LOW);
  delay(2);

  digitalWrite(TRIG,HIGH);
  delay(10);

  digitalWrite(TRIG,LOW);

  duration = pulseIn(ECHO, HIGH);

  distance = get_distance(duration);
  Serial.print("Distance: ");
  Serial.println(distance);

  delay(100);
}


float get_distance(float _duration){

  float _distance = (_duration*.0343)/2;
  return _distance;

}