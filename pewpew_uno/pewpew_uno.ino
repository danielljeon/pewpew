/**
 * Example catapult with ultrasonic ranging and fire button.
 */

#include <Servo.h>

Servo myServo;  // Servo object.

// HC-SR04 pins.
const int TRIG_PIN = 2;
const int ECHO_PIN = 3;

// Moving median filter settings.
const int MEDIAN_WINDOW = 5;
float distanceBuffer[MEDIAN_WINDOW];
int bufferIndex = 0;
int bufferCount = 0;

// Example curve fit solution.
float y_from_x(float x) {
  // Polynomial approximation generated from Python.
  float y = -0.00002389f * x * x * x + 0.00095641f * x * x + -0.54626373f * x + 97.09920332f;
  return y;
}

// Read one raw distance measurement from HC-SR04 (in cm).
float read_ultrasonic_cm() {
  // Ensure trigger is low.
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // 10 us pulse to trigger.
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo pulse duration.
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);  // timeout ~30 ms.

  if (duration == 0) {
    // No echo detected, return some large value or 0.
    return 0.0f;
  }

  // Speed of sound ~343 m/s => 0.0343 cm/us. Divide by 2 (there and back).
  float distance_cm = duration * 0.0343f / 2.0f;
  return distance_cm;
}

// Simple moving median filter over the last MEDIAN_WINDOW readings.
float get_filtered_distance_cm() {
  float d = read_ultrasonic_cm();

  // Store new reading in circular buffer.
  distanceBuffer[bufferIndex] = d;
  bufferIndex = (bufferIndex + 1) % MEDIAN_WINDOW;
  if (bufferCount < MEDIAN_WINDOW) {
    bufferCount++;
  }

  // Copy current buffer into temp array for sorting.
  float temp[MEDIAN_WINDOW];
  for (int i = 0; i < bufferCount; i++) {
    temp[i] = distanceBuffer[i];
  }

  // Simple bubble sort (small N so it's fine).
  for (int i = 0; i < bufferCount - 1; i++) {
    for (int j = 0; j < bufferCount - 1 - i; j++) {
      if (temp[j] > temp[j + 1]) {
        float t = temp[j];
        temp[j] = temp[j + 1];
        temp[j + 1] = t;
      }
    }
  }

  // Return median value.
  int mid = bufferCount / 2;
  return temp[mid];
}

void move_to_target(float distance_cm) {
  float angle_deg = y_from_x(distance_cm);
  Serial.print("Target: ");
  Serial.print(distance_cm);
  Serial.print(" cm, angle: ");
  Serial.print(angle_deg);
  Serial.println(" deg");
  myServo.write(angle_deg);
}

void setup() {
  Serial.begin(9600);
  myServo.attach(9);  // Servo signal wire pin 9.

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Optionally pre-fill the buffer with initial readings.
  for (int i = 0; i < MEDIAN_WINDOW; i++) {
    distanceBuffer[i] = read_ultrasonic_cm();
    bufferCount++;
  }
}

void loop() {
  float distance_cm = get_filtered_distance_cm();
  move_to_target(distance_cm);
  delay(200);  // Small delay between updates.
}
