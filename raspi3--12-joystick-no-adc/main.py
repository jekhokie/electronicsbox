#!/usr/bin/env python
#
# Prints out a relative time for an analog joystick connected to a Raspberry Pi 3 B+ without
# using an Analog to Digital converter. See README for details. Assumes the following wiring:
#
# - Joystick VCC to RasPi +3.3V (PIN1)
# - Joystick XOUT/HOR to 1k Ohm Resistor to RasPi GPIO26 (PIN37)
# - Joystick GND to 100nF Capacitor PIN1
# - 100nF Capacitor PIN2 to RasPi GND
# - 100nF Capacitor PIN1 to RasPi GPIO19 (PIN35)
# - Joystick GND to RasPi GND

import RPi.GPIO as GPIO
import time

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin to use for charging and sensor
CHARGE_PIN = 26
SENSE_PIN = 19

# thresholds for whether joystick is in left/center/right position
LEFT_THRESHOLD = 20
RIGHT_THRESHOLD = 48

# discharge capacitor to "ready" for sensor
def discharge_cap():
    '''
    1. stop charging operation
    2. convert measure pin to output
    3. set measure pin to low to discharge capacitor
       (wait small duration of time for discharge)
    '''
    GPIO.setup(CHARGE_PIN, GPIO.IN)
    GPIO.setup(SENSE_PIN, GPIO.OUT)
    GPIO.output(SENSE_PIN, False)
    time.sleep(0.005)

# charge the capacitor until sensor pin flips to "HIGH"
def get_charge_time():
    '''
    1. convert measure pin to input (start measurement)
    2. convert charge pin to output
    3. flip charge pin to "HIGH" (start charging capacitor)
    4. record time until measure pin converts to "HIGH" state
    '''
    count = 0

    # align pins appropriately
    GPIO.setup(SENSE_PIN, GPIO.IN) 
    GPIO.setup(CHARGE_PIN, GPIO.OUT)

    # start charging and measure
    GPIO.output(CHARGE_PIN, GPIO.HIGH)
    while(GPIO.input(SENSE_PIN) == GPIO.LOW):
        count = count +1

    return count

# main execution loop
while True:
    # discharge capacitor, then measure how long to convert
    # "SENSE_PIN" to "HIGH"
    discharge_cap()
    val = get_charge_time()

    # determine position based on thresholds
    pos = "UNKNOWN"
    if val < LEFT_THRESHOLD:
        pos = "LEFT"
    elif val >= LEFT_THRESHOLD and val <= RIGHT_THRESHOLD:
        pos = "CENTER"
    elif val > RIGHT_THRESHOLD:
        pos = "RIGHT"

    print("SENSOR: {} | POSITION: {}".format(val, pos))
    time.sleep(0.3)
