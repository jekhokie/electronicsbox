#!/usr/bin/env python
#
# Illuminate LEDs on a light bar graph connected to a Raspberry PI 3 B+. Assumes the
# following wiring:
#
# - LED BAR TOP PIN1 to RasPi GPIO14
# - LED BAR TOP PIN2 to RasPi GPIO15
# - LED BAR TOP PIN3 to RasPi GPIO18
# - LED BAR TOP PIN4 to RasPi GPIO23
# - LED BAR TOP PIN5 to RasPi GPIO24
# - LED BAR TOP PIN6 to RasPi GPIO25
# - LED BAR TOP PIN7 to RasPi GPIO8
# - LED BAR TOP PIN8 to RasPi GPIO7
# - LED BAR TOP PIN9 to RasPi GPIO1
# - LED BAR TOP PIN10 to RasPi GPIO12
# - LED BAR BOTTOM (ALL PINS) to Resistor Network
# - Resistor Network PIN1 (dot) to RasPi GND

import RPi.GPIO as GPIO
import time

# identify the GPIO pin to use
SWITCH_STATE1_PIN = 17
SWITCH_STATE2_PIN = 27

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set the pins being used to control the LEDs
LED_PINS = [14, 15, 18, 23, 24, 25, 8, 7, 1, 12]

# configure all pins as output drivers
for led in LED_PINS:
    GPIO.setup(led, GPIO.OUT, initial=0)

# loop through LED list and illuminate each LED in sequence, then
# turn them off in reverse sequence
try:
    while True:
        # turn on in sequence
        for led in LED_PINS:
            GPIO.output(led, 1)
            time.sleep(0.1)

        # shut off in sequence
        for led in LED_PINS:
            GPIO.output(led, 0)
            time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
