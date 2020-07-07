#!/usr/bin/env python
#
# Prints the analog value of an analog joystick connected to the Raspberry Pi 3 B+ using SPI
# through an MCP3008 Analog to Digital converter chip (ADC).
# See README for wiring details.

import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# thresholds for whether joystick is in left/center/right/up/down position
MIN_THRESHOLD = 30000
MAX_THRESHOLD = 40000

# create SPI bus, chip select, and resulting mcp object
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# create analog input on channel 0 for x-axis, channel 1 for y-axis
x_chan = AnalogIn(mcp, MCP.P0)
y_chan = AnalogIn(mcp, MCP.P1)

# main execution loop
while True:
    # perform one-time lookup of values
    x_val = x_chan.value
    x_volt = x_chan.voltage
    y_val = y_chan.value
    y_volt = y_chan.voltage

    # initialize direction
    x_pos = "UNKNOWN"
    y_pos = "UNKNOWN"

    # calculate direction for x
    x_pos = "UNKNOWN"
    if x_val < MIN_THRESHOLD:
        x_pos = "LEFT"
    elif x_val >= MIN_THRESHOLD and x_val <= MAX_THRESHOLD:
        x_pos = "CENTER"
    elif x_val > MAX_THRESHOLD:
        x_pos = "RIGHT"

    # calculate direction for y
    y_pos = "UNKNOWN"
    if y_val < MIN_THRESHOLD:
        y_pos = "DOWN"
    elif y_val >= MIN_THRESHOLD and y_val <= MAX_THRESHOLD:
        y_pos = "CENTER"
    elif y_val > MAX_THRESHOLD:
        y_pos = "UP"

    # print raw values
    print("X-DIR: {} | Y-DIR: {}".format(x_pos, y_pos))
    print("\tXVAL/XVOLT: {}/{}V | YVAL/YVOLT: {}/{}V".format(x_chan.value, str(x_chan.voltage), y_chan.value, str(y_chan.voltage)))

    time.sleep(0.5)
