/**
 * Example catapult with ultrasonic ranging and fire button.
 */

#include <Servo.h>

Servo myServo;  // Servo object.

// Example curve fit solution.
float y_from_x(float x) {
  // Polynomial approximation generated from Python.
  float y = -0.00002389f * x * x * x + 0.00095641f * x * x + -0.54626373f * x + 97.09920332f;
  return y;
}

float move_to_target(float distance_cm) {
  float angle_deg = y_from_x(distance_cm);
  Serial.print("\tTarget: ");
  Serial.print(distance_cm);
  Serial.print(" cm, angle: ");
  Serial.print(angle_deg);
  Serial.print(" deg");
  myServo.write(angle_deg);
}

void setup() {
  Serial.begin(9600);
  myServo.attach(9);  // Servo signal wire pin 9.
}

void loop() {
  move_to_target(50.0f);  // Example distance target.
}
