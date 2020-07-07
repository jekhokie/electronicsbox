#!/usr/bin/env python
#
# Iterate through digits on a 7-segment LED display (common cathode variant).
# Assumes the following configuration for the display:
#
# G F COM A B
# | |  |  | |
# |---------|
# |    A    |
# | F     B |
# |    G    |
# | E     C |
# |    D  dp|
# |---------|
# | |  |  | |
# E D COM C DP
# 
# Based on the above, assumes the following wiring (based on BCM pin numbering):
#
# - LED G to 220 Ohm Resistor to RasPi GPIO2 (PIN3)
# - LED F to 220 Ohm Resistor to RasPi GPIO3 (PIN5)
# - LED A to 220 Ohm Resistor to RasPi GPIO4 (PIN7)
# - LED B to 220 Ohm Resistor to RasPi GPIO17 (PIN11)
# - LED E to 220 Ohm Resistor to RasPi GPIO27 (PIN13)
# - LED D to 220 Ohm Resistor to RasPi GPIO22 (PIN15)
# - LED C to 220 Ohm Resistor to RasPi GPIO10 (PIN19)
# - LED DP (not wired)
# - LED COM (BOTH) to RasPi GND
 
import RPi.GPIO as GPIO
import time

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set the pins being used to control the LEDs
#LED_PINS = [2, 3, 4, 9, 10, 17, 22, 27]

# store the ordered A-G pins for output
#             A  B   C   D   E   F  G
DIGIT_PINS = [4, 17, 10, 22, 27, 3, 2]

# configure all pins as output drivers
for led in DIGIT_PINS:
    GPIO.setup(led, GPIO.OUT, initial=1)

# define segments for displaying digits
# in order, left to right in array are segments:
#
# A, B, C, D, E, F, G
#
# referencing above  diagram of segments to light up:
#
# G F COM A B
# | |  |  | |
# |---------|
# |    A    |
# | F     B |
# |    G    |
# | E     C |
# |    D  dp|
# |---------|
# | |  |  | |
# E D COM C DP
#
# this means, for instance, if we want to show "2", we need to
# light segments A, B, G, E, D, which corresponds to [1, 1, 0, 1, 1, 0, 1]
digit0 = [1, 1, 1, 1, 1, 1, 1]
digit1 = [0, 1, 1, 0, 0, 0, 0]
digit2 = [1, 1, 0, 1, 1, 0, 1]
digit3 = [1, 1, 1, 1, 0, 0, 1]
digit4 = [0, 1, 1, 0, 0, 1, 1]
digit5 = [1, 0, 1, 1, 0, 1, 1]
digit6 = [1, 0, 1, 1, 1, 1, 1]
digit7 = [1, 1, 1, 0, 0, 0, 0]
digit8 = [1, 1, 1, 1, 1, 1, 1]
digit9 = [1, 1, 1, 0, 0, 1, 1]

# store all digits in array for easy parsing
digit_list = [digit0, digit1, digit2, digit3, digit4,
              digit5, digit6, digit7, digit8, digit9]

# function to clear the LED screen
def clear_screen():
    for d in range(0, 7):
        GPIO.output(DIGIT_PINS[d], 0)

# light up a digit
def write_digit(digit):
    for x in range(0, 7):
        GPIO.output(DIGIT_PINS[x], digit[x])

# loop through digit list and display each digit in sequence
try:
    while True:
        # print digits 0-9 in sequence
        for digit in digit_list:
            clear_screen()
            write_digit(digit)
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
