#!/usr/bin/env python3
#
# Acts as a receiver of data from a sending XBee module, and controls
# LEDs (up, down, left, right) associated with the codes sent by the trasmitter.
# See README for additional information.
#
# **NOTE: REQUIRES PYTHON 3**

import serial, time
import RPi.GPIO as GPIO
from xbee import XBee

# assign the LED pins and XBee device settings
LED_UP_PIN = 21
LED_DOWN_PIN = 20
LED_LEFT_PIN = 16
LED_RIGHT_PIN = 12
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# set the pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# initialize GPIO outputs for LEDs
for l in [LED_UP_PIN, LED_DOWN_PIN, LED_LEFT_PIN, LED_RIGHT_PIN]:
    GPIO.setup(l, GPIO.OUT)

# handler for whenever data is received from transmitters - operates asynchronously
def receive_data(data):
    print("Received data: {}".format(data))
    rx = data['rf_data'].decode('utf-8')
    state, led = rx[:1], rx[1:]

    # parse the received contents and activate the respective LED if the data
    # received is actionable
    if state in ("0", "1"):
        if led in ("UP", "DOWN", "LEFT", "RIGHT"):
            # TODO: Use some meta-programming here to translate received led and state
            #       to the actual LED state, removing all conditionals
            if led == "UP":
                GPIO.output(LED_UP_PIN, int(state))
            elif led == "DOWN":
                GPIO.output(LED_DOWN_PIN, int(state))
            elif led == "LEFT":
                GPIO.output(LED_LEFT_PIN, int(state))
            elif led == "RIGHT":
                GPIO.output(LED_RIGHT_PIN, int(state))
        else:
            print("ERROR: Received invalid LED '{}' - ignoring transmission".format(state))
    else:
        print("ERROR: Received invalid STATE '{}' - ignoring transmission".format(state))

    print("Packet: {}".format(data))
    print("Data: {}".format(data['rf_data']))

# configure the xbee and enable asynchronous mode
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, callback=receive_data, escaped=False)

while True:
    try:
        # operate in async mode where all messages will go to handler
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

# clean up
GPIO.cleanup()
xbee.halt()
ser.close()
