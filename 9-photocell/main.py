#!/usr/bin/env python
#
# Prints out the value of a photocell connected to the Raspberry PI 3 B+. Since the Raspberry PI
# 3 does not have analog inputs, the circuit designed simulates analog translation. Assumes the following
# wiring for the circuit:
# 
# - Photocell LEG1 to RasPi GPIO2 (PIN3)
# - Photocell LEG2 to RasPi GND
# - 1uF Capacitor POS to Photocell LEG1/RasPi GPIO2
# - 1uF Capacitor NEG to RasPi GND
 
import RPi.GPIO as GPIO
import time

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin to use for photocell
PHOTOCELL_PIN = 2

# calculate time for capacitor to fill, indicating photocell resistance
def photocell_time():
    c = 0

    # drain the capacitor
    GPIO.setup(PHOTOCELL_PIN, GPIO.OUT)
    GPIO.output(PHOTOCELL_PIN, GPIO.LOW)
    time.sleep(0.1)

    # revert pin to input, and count until pin flips to HIGH
    GPIO.setup(PHOTOCELL_PIN, GPIO.IN)
    while(GPIO.input(PHOTOCELL_PIN) == GPIO.LOW):
        c += 1

    return c

# loop printing out values
try:
    while True:
        print("TIME: {}".format(photocell_time()))
except KeyboardInterrupt:
    GPIO.cleanup()
