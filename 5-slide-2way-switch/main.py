#!/usr/bin/env python
#
# Detect and print the status of a 2 state, 3 wire switch connected to a Raspberry PI
# 3 B+. Assumes the following wiring:
#
# - SWITCH MIDDLE PIN to RasPi +3.3V
# - SWITCH LEFT PIN to RasPi GPIO17
# - SWITCH RIGHT PIN to RasPi GPIO27
# - SWITCH LEFT PIN to 10k Ohm Resistor to RasPi GND (parallel)
# - SWITCH RIGHT PIN to 10k Ohm Resistor to RasPi GND (parallel)

import RPi.GPIO as GPIO
import time

# identify the GPIO pin to use
SWITCH_STATE1_PIN = 17
SWITCH_STATE2_PIN = 27

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set the SWITCH pins to input
GPIO.setup(SWITCH_STATE1_PIN, GPIO.IN)
GPIO.setup(SWITCH_STATE2_PIN, GPIO.IN)

# continuously check and print state of switch
while True:
    if (GPIO.input(SWITCH_STATE1_PIN) == 1):
        print("Switch in Position 1 (LEFT)")
    elif (GPIO.input(SWITCH_STATE2_PIN) == 1):
        print("Switch in Position 2 (RIGHT)")
    else:
        print("Error: Unable to detect switch state")

    time.sleep(1)
