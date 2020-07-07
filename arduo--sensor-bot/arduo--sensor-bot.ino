#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <HCSR04.h>
#include <SPI.h> // Not actualy used but needed to compile

String xPos, yPos, selPos;
int xSpeed, ySpeed;
int i;

// set up the motor shield
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(3);  // GPIO3
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(4);  // GPIO4

// set up the distance sensor
// GPIO13 trigger pin
// GPIO12 echo pin
UltraSonicDistanceSensor distanceSensor(13, 12);

void setup() {
  // initialize Serial communication
  Serial.begin(9600);
  Serial.println("SensorBot!");

  // initialize the motor drivers
  AFMS.begin();
}

void loop() {
  // capture and output sensor data
  int obstacleDistanceCm = distanceSensor.measureDistanceCm();
  Serial.println("Distance sensor value: " + (String)obstacleDistanceCm);

  // default to 50% speed
  int speed = 128;

  /*
  // useful for if you add a potentiometer to control the speed
  int sensorSpeed = analogRead(0);
  Serial.println("Speed sensor value: " + (String)sensorSpeed);
  int speed = map(sensorSpeed, 0, 1023, 0, 255);
  Serial.println("Speed: " + (String)speed);
  */

  // set the speed for the motors
  myMotor1->setSpeed(speed);
  myMotor2->setSpeed(speed);

  // move the motor based on potentiometer speed mapping
  // and turn if approaching an obstacle
  if (obstacleDistanceCm <= 20) {
    Serial.println("Turning");
    myMotor1->run(FORWARD);
    myMotor2->run(BACKWARD);  
  } else {
    Serial.println("Going Forward");
    myMotor1->run(FORWARD);
    myMotor2->run(FORWARD);
  }

  delay(250);
}
