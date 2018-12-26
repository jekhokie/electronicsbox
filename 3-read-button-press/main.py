#!/usr/bin/env python
#
# Reads button status and reports whether the button has been pressed
# or is currently depressed when connected to a Raspberry PI 3 B+.
# Assumes the following wiring:
#
# - Button END1 to RasPi GND
# - Button END2 to RasPi GPIO13
#
# Credit: http://razzpisampler.oreilly.com/ch07.html

import RPi.GPIO as GPIO
import time

# set the pin mode
GPIO.setmode(GPIO.BCM)

# assign the current pin for GPIO
BUTTON_GPIO = 13

# set the GPIO pin to pull-up input mode
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# attempt to read the state of the button and print the result
while True:
  input_state = GPIO.input(BUTTON_GPIO)

  if input_state == False:
    print("Button Pressed")
  else:
    print("Button Depressed")

  time.sleep(0.2)
