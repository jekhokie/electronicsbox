#!/usr/bin/env python
#
# Blink an LED (simple circuit) using the GPIO library on a Raspberry
# PI 3 B+. Assumes the following wiring:
#
# - LED NEG(-) to 1k Resistor to RasPi GND
# - LED POS(+) to RasPi GPIO26

import RPi.GPIO as GPIO
import time

# identify the GPIO pin to use
LED_PIN = 26

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set the LED pin to output
GPIO.setup(LED_PIN, GPIO.OUT)

# continuously blink LED
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
