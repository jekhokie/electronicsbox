#!/usr/bin/env python
#
# Print the Raspberry PI IP address and current date/time to a 16x4 character LCD display
# on a Raspberry PI 3 B+ using 4-bit wiring/programming. Assumes the following wiring:
#
# - LCD PIN1 (VSS) to RasPi GND
# - LCD PIN2 (VDD) to RasPi +5V
# - LCD PIN3 (VO) to POT1 CENTER PIN
# - LCD PIN4 (RS) to RasPi GPIO26 (BCM PIN37)
# - LCD PIN5 (RW) to RasPi GND
# - LCD PIN6 (E) to RasPi GPIO19 (BCM PIN35)
# - LCD PIN7-PIN10 (NOT USED)
# - LCD PIN11 (D4) to RasPi GPIO13 (BCM PIN33)
# - LCD PIN12 (D5) to RasPi GPIO6 (BCM PIN31)
# - LCD PIN13 (D6) to RasPi GPIO5 (BCM PIN29)
# - LCD PIN14 (D7) to RasPi GPIO11 (BCM PIN23)
# - LCD PIN15 (A) to POT2 RIGHT PIN
# - LCD PIN16 (K) to RasPi GND
# - POT1 RIGHT PIN to RasPi GND
# - POT2 CENTER PIN to RasPi +5V
#
# Ref: https://rplcd.readthedocs.io/en/stable/getting_started.html

import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

GPIO.setwarnings(False)

# initialize the LCD
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],
              numbering_mode=GPIO.BOARD)

# write 2 lines of text
lcd.cursor_pos = (0, 0)
lcd.write_string(u'Hello world!')
lcd.cursor_pos = (1, 0)
lcd.write_string(u'This is a test!')

# wait for 5 seconds
print("Sleeping for 5 seconds...")
time.sleep(5)

# clear the LCD and pins
lcd.clear()
print("LCD cleared!")
GPIO.cleanup()
