#!/usr/bin/env python
#
# Integration with an Adafruit Arduino Motor Shield (V2) (http://www.adafruit.com/products/1438).
# Although this shield is built for the Arduino series boards, it can be modified/used in other
# applications. This tutorial will use the board connected to a Raspberry Pi 3 B+ with the following
# pin configurations ("Arduino Motor Controller Shield" referenced as "AMC" below). Note that this
# tutorial uses a DC motor:
#
# - AMC VCC screw terminal connected to *external* +5V Power Supply VCC - powers motors
# - AMC M1 (2-pin) screw terminal connected to Wire1 and Wire2 on DC Motor
# - AMC +5V pin connected to RasPi +5V (PIN2) - powers chips/circuitry on board
# - AMC SCL pin connected to RasPi SCL1 (PIN5)
# - AMC SDA pin connected to RasPi SDA1 (PIN3)
# - RasPi GND/Motor Shield GND Pin/External +5V GND all connected (Common Ground)
#
# Code basis built from the following file:
#   https://raw.githubusercontent.com/adafruit/Adafruit-Motor-HAT-Python-Library/master/examples/DCTest.py

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time

# default I2C communication - all Arduino Motor Shields ship with
# address 0x60 as referenceable I2C address
mh = Adafruit_MotorHAT(addr=0x60)
motor1 = mh.getMotor(1)

# output some debugging information about the pins for the motor
print("Motor Details:")
print("PWM PIN: {}".format(motor1.PWMpin))
print("IN1 PIN: {}".format(motor1.IN1pin))
print("IN2 PIN: {}".format(motor1.IN2pin))
print("------------------------------------")

# main execution loop
while (True):
    try:
        print("Spinning Forward...")
        motor1.run(Adafruit_MotorHAT.FORWARD)

        print("\tSpeed up...")
        for i in range(255):
            motor1.setSpeed(i)
            time.sleep(0.01)

        print("\tSlow down...")
        for i in reversed(range(255)):
            motor1.setSpeed(i)
            time.sleep(0.01)

        print("Spinning Backward...")
        motor1.run(Adafruit_MotorHAT.BACKWARD)

        print("\tSpeed up...")
        for i in range(255):
            motor1.setSpeed(i)
            time.sleep(0.01)

        print("\tSlow down...")
        for i in reversed(range(255)):
            motor1.setSpeed(i)
            time.sleep(0.01)

        time.sleep(1.0)
    except KeyboardInterrupt:
        break

# release the motor
mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
