#!/usr/bin/env python3
#
# Receiver which receives commands from the controller and controls the robot.
# See README for wiring.
#
# To get this script to trigger automatically, first load the directory onto
# the raspberry pi and execute the following commands to build the environment
# virtualenv setup and install the dependent libraries:
#
#  virtualenv .env
#  pip install -r requirements.txt
#
# To enable the script to launch automatically, edit the /etc/rc.local file on
# the Raspberry Pi which controls the robot and enter the following commands
# right before the 'exit 0' command:
# 
#   cd /home/pi/Desktop/raspi-projects/15-joystick-adc-with-arduino-motor-shield
#   . .env/bin/activate
#   python robot.py
#
# Following this, reboot the Raspberry Pi and the green LED will light up when
# communication is ready to be received (the robot is ready to be controlled).

import serial, time
import RPi.GPIO as GPIO
from xbee import XBee
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

# assign the pins and XBee device settings
HORN_PIN = 19
READY_PIN = 21
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# set the pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set up the horn and ready pins as output
GPIO.setup(HORN_PIN, GPIO.OUT)
GPIO.setup(READY_PIN, GPIO.OUT)

# set up the motor controllers
mh = Adafruit_MotorHAT(addr=0x60)
left_motor = mh.getMotor(1)
right_motor = mh.getMotor(2)

# handler for whenever data is received from transmitters - operates asynchronously
def receive_data(data):
    print("Received data: {}".format(data))
    rx = data['rf_data'].decode('utf-8')

    # sanity check we received the correct number of inputs for horn, left, and right motor
    if len(rx) != 3:
        print("received invalid data: {}".format(rx))
        return

    # gather the control signals
    horn, l_motor, r_motor = rx[0], rx[1], rx[2]

    # parse the received contents and take action as appropriate
    # received is actionable
    # - horn control
    if horn == "1":
        GPIO.output(HORN_PIN, GPIO.HIGH)
    else:
        GPIO.output(HORN_PIN, GPIO.LOW)

    # - motor movement for left motor control
    if l_motor == "0":
        left_motor.run(Adafruit_MotorHAT.BACKWARD)
        left_motor.setSpeed(255)
    elif l_motor == "1":
        left_motor.run(Adafruit_MotorHAT.RELEASE)
        left_motor.setSpeed(0)
    elif l_motor == "2":
        left_motor.run(Adafruit_MotorHAT.FORWARD)
        left_motor.setSpeed(255)
    else:
        print("Invalid entry for left motor control: {}".format(lmc))

    # - motor movement for right motor control
    if r_motor == "0":
        right_motor.run(Adafruit_MotorHAT.BACKWARD)
        right_motor.setSpeed(255)
    elif r_motor == "1":
        right_motor.run(Adafruit_MotorHAT.RELEASE)
        right_motor.setSpeed(0)
    elif r_motor == "2":
        right_motor.run(Adafruit_MotorHAT.FORWARD)
        right_motor.setSpeed(255)
    else:
        print("Invalid entry for right motor control: {}".format(lmc))

    print("Packet: {}".format(data))
    print("Data: {}".format(data['rf_data']))

# configure the xbee and enable asynchronous mode
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, callback=receive_data, escaped=False)

# trigger the "I'm ready" LED
GPIO.output(READY_PIN, GPIO.HIGH)

# main execution loop
while True:
    try:
        # operate in async mode where all messages will go to handler
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

# clean up
GPIO.cleanup()
xbee.halt()
left_motor.run(Adafruit_MotorHAT.RELEASE)
right_motor.run(Adafruit_MotorHAT.RELEASE)
ser.close()
