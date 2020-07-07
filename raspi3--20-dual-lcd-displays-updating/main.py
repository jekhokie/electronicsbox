#!/usr/bin/env python
#
# Print various information on 2x LCD displays:
#
#   LCD_4X: 16x4 characters without a backlight
#      - LCD_4X_POT1: potentiometer for contrast control
#   LCD_2X: 16x2 characters with a mono (single color/white) backlight
#      - LCD_2X_POT1: potentiometer for contrast control
#      - LCD_2X_POT2: potentiometer for backlight brightness control
#
# Assumes the following wiring:
#
#  - LCD_4X PIN1 (VSS) to RasPi GND
#  - LCD_4X PIN2 (VDD) to RasPi +5V
#  - LCD_4X PIN3 (VO) to LCD_4X_POT1 CENTER PIN
#  - LCD_4X PIN4 (RS) to RasPi GPIO26
#  - LCD_4X PIN5 (RW) to RasPi GND
#  - LCD_4X PIN6 (EN) to RasPi GPIO19 
#  - LCD_4X PIN7-PIN10 (NOT USED)
#  - LCD_4X PIN11 (D4) to RasPi GPIO25
#  - LCD_4X PIN12 (D5) to RasPi GPIO24
#  - LCD_4X PIN13 (D6) to RasPi GPIO22
#  - LCD_4X PIN14 (D7) to RasPi GPIO27
#  - LCD_4X PIN15 (A) (NOT USED - NO BACKLIGHT)
#  - LCD_4X PIN16 (K) (NOT USED - NO BACKLIGHT)
#  - LCD_4X_POT1 RIGHT PIN to RasPi GND
#  - LCD_4X_POT1 LEFT PIN to RasPi +5V
#  
#  - LCD_2X PIN1 (VSS) to RasPi GND
#  - LCD_2X PIN2 (VDD) to RasPi +5V
#  - LCD_2X PIN3 (VO) to LCD_2X_POT1 CENTER PIN
#  - LCD_2X PIN4 (RS) to RasPi GPIO2
#  - LCD_2X PIN5 (RW) to RasPi GND
#  - LCD_2X PIN6 (EN) to RasPi GPIO3
#  - LCD_2X PIN7-PIN10 (NOT USED)
#  - LCD_2X PIN11 (D4) to RasPi GPIO13
#  - LCD_2X PIN12 (D5) to RasPi GPIO6
#  - LCD_2X PIN13 (D6) to RasPi GPIO5
#  - LCD_2X PIN14 (D7) to RasPi GPIO11
#  - LCD_2X PIN15 (LED Anode) to LCD_2X_POT2 RIGHT PIN
#  - LCD_2X PIN16 (LED Cathode) to RasPi GPIO14
#  - LCD_2X_POT1 RIGHT PIN to RasPi GND
#  - LCD_2X_POT2 CENTER PIN to RasPi +5V
#

import time
import ntplib
import board
import digitalio
import pytz
import adafruit_character_lcd.character_lcd as characterlcd
import netifaces as ni
from signal import signal, SIGINT
from datetime import datetime, timedelta
from pytz import timezone

# configuration constants
#   TIMEZONE: timezone for displaying local time
#   NTP_SERVER: endpoint to query for NTP time updates
#   TIME_RESET_MIN: how many minutes (appox.) to wait between
#                   querying NTP for time drift reset
#   ITER_SLEEP_SEC: how many seconds to sleep for each period
#                   (between data updates)
TIMEZONE       = 'US/Eastern'
NTP_SERVER     = 'us.pool.ntp.org'
TIME_RESET_MIN = 1
ITER_SLEEP_SEC = 1

# 16x4 LCD - no backlight
LCD_4X_RS   = digitalio.DigitalInOut(board.D26)
LCD_4X_EN   = digitalio.DigitalInOut(board.D19)
LCD_4X_D7   = digitalio.DigitalInOut(board.D27)
LCD_4X_D6   = digitalio.DigitalInOut(board.D22)
LCD_4X_D5   = digitalio.DigitalInOut(board.D24)
LCD_4X_D4   = digitalio.DigitalInOut(board.D25)
LCD_4X_COLS = 16
LCD_4X_ROWS = 4

# 16x2 LCD - mono-backlight
LCD_2X_RS   = digitalio.DigitalInOut(board.D2)
LCD_2X_EN   = digitalio.DigitalInOut(board.D3)
LCD_2X_D7   = digitalio.DigitalInOut(board.D11)
LCD_2X_D6   = digitalio.DigitalInOut(board.D5)
LCD_2X_D5   = digitalio.DigitalInOut(board.D6)
LCD_2X_D4   = digitalio.DigitalInOut(board.D13)
LCD_2X_COLS = 16
LCD_2X_ROWS = 2
LCD_2X_BL   = digitalio.DigitalInOut(board.D14)

# counter for various interval updates
seq = 0

# timezone object for conversions
tz = pytz.timezone(TIMEZONE)

def resetDisplays():
    '''Clear displays and disable backlights'''
    lcd_4x.clear()
    lcd_2x.backlight = False
    lcd_2x.clear()

def terminateProgram(sig, frame):
    '''Handle a CTRL-C action'''
    print('SIGINT/CTRL-C signal sent - terminating')

    # reset the LCDs and exit gracefully
    resetDisplays()
    exit(0)

def getDeviceIP():
    '''Get the wireless IP address for this device'''
    return ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

def getDateTimeNTP():
    '''Get accurate date/time information from NTP'''
    try:
        c = ntplib.NTPClient()
        response = c.request(NTP_SERVER, version=3)
        dt = datetime.fromtimestamp(response.tx_time, tz=tz)
    except:
        dt = -1

    return dt

if __name__ == "__main__":
    # catch SIGINT
    signal(SIGINT, terminateProgram)

    # initialize the 2x LCD displays
    lcd_4x = characterlcd.Character_LCD_Mono(
                    LCD_4X_RS, LCD_4X_EN,
                    LCD_4X_D4, LCD_4X_D5, LCD_4X_D6, LCD_4X_D7,
                    LCD_4X_COLS, LCD_4X_ROWS)
    lcd_2x = characterlcd.Character_LCD_Mono(
                    LCD_2X_RS, LCD_2X_EN,
                    LCD_2X_D4, LCD_2X_D5, LCD_2X_D6, LCD_2X_D7,
                    LCD_2X_COLS, LCD_2X_ROWS,
                    backlight_pin=LCD_2X_BL,
                    backlight_inverted=True)
    lcd_2x.backlight = True

    # query for IP address only once - this is not likely to change
    # unless the device is rebooted or the lease expires (not likely)
    ip = getDeviceIP()

    # continuously loop through capabilities and update
    # information on intermittent basis
    while True:
        try:
            # perform an NTP sync to account for drift
            # every TIME_RESET_MIN minutes, else, get the time
            # locally based on the OS time
            if seq > (TIME_RESET_MIN * 5):
                seq = 0

                # attempt to get the date and time from NTP - fall
                # back to converted OS time if necessary
                dt = getDateTimeNTP()
                if dt == -1:
                    dt = datetime.now(tz)
            else:
                seq += 1
                dt = datetime.now(tz)

            # convert the date and time to readable formats
            curdate = dt.strftime("%b %d, %Y")
            curtime = dt.strftime("%I:%M:%S %p")

            # print messages on each LCD
            lcd_4x.message = f"{ip}\n{curdate}\n{curtime}"
            lcd_2x.message = "Hello 2x\nCircuitPython!"
            time.sleep(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            resetDisplays()
            exit(1)
