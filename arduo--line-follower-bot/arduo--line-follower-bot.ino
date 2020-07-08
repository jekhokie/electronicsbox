//#include <Wire.h>
#include <Adafruit_MotorShield.h>
//#include <SPI.h> // Not actualy used but needed to compile

// configs for IR sensors
const int irSensorLeft = 7;
const int irSensorRight = 8;

// configs for default speed
const int speed = 128;    // max speed == 256

// vars //
int leftSensorData;
int rightSensorData;

// set up the motor shield
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(3);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(4);

void setup() {
  // initialize Serial communication
  Serial.begin(9600);
  Serial.println("Line Sensor Bot!");

  // initialize the IR sensor pins
  pinMode(irSensorLeft, INPUT);
  pinMode(irSensorRight, INPUT);

  // initialize the motor drivers
  AFMS.begin();
}

void loop() {
  // capture and output sensor data
  leftSensorData = digitalRead(irSensorLeft);
  rightSensorData = digitalRead(irSensorRight);
  Serial.println("Left IR sensor value: " + (String)leftSensorData);
  Serial.println("Right IR sensor value: " + (String)rightSensorData);

  // set the speed for the motors
  myMotor1->setSpeed(speed);
  myMotor2->setSpeed(speed);

  // determine next course of action
  if (leftSensorData == HIGH && rightSensorData == HIGH) {    // on track - straight
    myMotor1->run(FORWARD);
    myMotor2->run(FORWARD);
  }
  if (leftSensorData == HIGH && rightSensorData == LOW) {    // veering left - turn right to adjust
    myMotor1->run(FORWARD);
    myMotor2->run(RELEASE);
  }
  if (leftSensorData == LOW && rightSensorData == HIGH) {    // veering right - turn left to adjust
    myMotor1->run(RELEASE);
    myMotor2->run(FORWARD);
  }
  if (leftSensorData == LOW && rightSensorData == LOW) {    // end tape - stop
    myMotor1->run(RELEASE);
    myMotor2->run(RELEASE);
  }

  delay(250);
}
