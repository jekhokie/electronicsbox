#!/usr/bin/env python3
#
# Acts as a transmitter of data to a receiving XBee module. Sends commands
# based on push-buttons connected to the device.
#
# **NOTE: REQUIRES PYTHON 3**

import RPi.GPIO as GPIO
import serial
import time
from xbee import XBee

# assign the button pins and XBee device settings
BUTTON_UP_PIN = 19
BUTTON_DOWN_PIN = 13
BUTTON_LEFT_PIN = 6
BUTTON_RIGHT_PIN = 5
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# set the pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# initialize GPIO inputs for buttons
for b in [BUTTON_UP_PIN, BUTTON_DOWN_PIN, BUTTON_LEFT_PIN, BUTTON_RIGHT_PIN]:
    GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure the xbee
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, escaped=False)

# handler for sending data to a receiving XBee device
def send_data(data):
    xbee.send("tx", dest_addr=b'\x00\x00', data=bytes("{}".format(data), 'utf-8'))

# send data to the receiver
send_data("Test")

# initialize previous states
last_up_state = False
last_down_state = False
last_left_state = False
last_right_state = False

# TODO: Send initialization to ensure all LEDs are off

while True:
    try:
        # obtain current state of each button
        up_state = GPIO.input(BUTTON_UP_PIN)
        down_state = GPIO.input(BUTTON_DOWN_PIN)
        left_state = GPIO.input(BUTTON_LEFT_PIN)
        right_state = GPIO.input(BUTTON_RIGHT_PIN)

        # check if button changed for "up"
        if up_state != last_up_state:
            last_up_state = up_state
            if up_state == False:
                print("Pressed up")
            else:
                print("Released up")

        # check if button changed for "down"
        if down_state != last_down_state:
            last_down_state = down_state
            if down_state == False:
                print("Pressed down")
            else:
                print("Released down")

        # check if button changed for "left"
        if left_state != last_left_state:
            last_left_state = left_state
            if left_state == False:
                print("Pressed left")
            else:
                print("Released left")

        # check if button changed for "right"
        if right_state != last_right_state:
            last_right_state = right_state
            if right_state == False:
                print("Pressed right")
            else:
                print("Released right")

        time.sleep(0.2)
    except KeyboardInterrupt:
        break

# clean up
GPIO.cleanup()
xbee.halt()
ser.close()
