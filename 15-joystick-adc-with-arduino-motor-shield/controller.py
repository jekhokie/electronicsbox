#!/usr/bin/env python
#
# Controller for robot actions. Able to perform actions such as:
#   - Forward
#   - Reverse
#   - Turn Right
#   - Turn Left
#   - Buzz Horn
#
# Uses the XBee device to communicate with robot target (see README for wiring).

import busio
import digitalio
import board
import time
import serial
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
from xbee import XBee
from adafruit_mcp3xxx.analog_in import AnalogIn

# set the pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# thresholds for whether joystick is in left/center/right/up/down position
MIN_THRESHOLD = 30000
MAX_THRESHOLD = 40000

# configure pins as appropriate
MCP_CS_PIN = board.D5       # MCP3008 CS
MCP_MISO_PIN = board.MISO   # MCP3008 MISO
MCP_MOSI_PIN = board.MOSI   # MCP3008 MOSI
MCP_SCK_PIN = board.SCK     # MCP3008 SCLK
JOY_X_MCP_IN = MCP.P0       # MCP3008 Joystick X-Axis Input (CH0)
JOY_Y_MCP_IN = MCP.P1       # MCP3008 Joystick Y-Axis Input (CH1)
BUTTON_PIN = 13             # joystick select for horn/buzzer
SERIAL_PORT = "/dev/ttyS0"  # serial port for xbee usage
BAUD_RATE = 9600            # baud rate for xbee communication

# ADC setup - create SPI bus, chip select, and resulting mcp object
spi = busio.SPI(clock=MCP_SCK_PIN, MISO=MCP_MISO_PIN, MOSI=MCP_MOSI_PIN)
cs = digitalio.DigitalInOut(MCP_CS_PIN)
mcp = MCP.MCP3008(spi, cs)

# create analog inputs for the joystick on the MCP3008, and set up joystick horn button
x_chan = AnalogIn(mcp, JOY_X_MCP_IN)
y_chan = AnalogIn(mcp, JOY_Y_MCP_IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure the xbee
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, escaped=False)

# handler for sending data to a receiving XBee device
def send_data(data):
    xbee.send("tx", dest_addr=b'\x00\x00', data=bytes("{}".format(data), 'utf-8'))

# main execution loop
while True:
    try:
        # perform one-time lookup of values for joystick
        x_val = x_chan.value
        x_volt = x_chan.voltage
        y_val = y_chan.value
        y_volt = y_chan.voltage
        buzzer = GPIO.input(BUTTON_PIN)

        # calculate motor control on/off based on following scheme:
        #       <BUZZER><LEFT_MOTOR><RIGHT_MOTOR>
        # where the BUZZER is either 0 or 1 and each motor
        # value is either a 0 (reverse), 1 (stop), or 2 (forward)
        # first, the buzzer
        control = "0"
        if buzzer == False:
            control = "1"

        # next, the motors
        # - brake: both off
        if x_val >= MIN_THRESHOLD and x_val <= MAX_THRESHOLD and y_val >= MIN_THRESHOLD and y_val <= MAX_THRESHOLD:
            print("brake")
            control = "{}{}{}".format(control, 1, 1)
        # - forward and reverse
        elif x_val >= MIN_THRESHOLD and x_val <= MAX_THRESHOLD:
            # - forward: left on forward, right on forward
            if y_val > MAX_THRESHOLD:
                print("forward")
                control = "{}{}{}".format(control, 2, 2)
            # - reverse: left on reverse, right on reverse
            elif y_val < MIN_THRESHOLD:
                print("reverse")
                control = "{}{}{}".format(control, 0, 0)
        # - left and right
        elif y_val >= MIN_THRESHOLD and y_val <= MAX_THRESHOLD:
            # - left: left on reverse, right on forward
            if x_val < MIN_THRESHOLD:
                print("left")
                control = "{}{}{}".format(control, 0, 2)
            # - right: left on forward, right on reverse
            elif x_val > MAX_THRESHOLD:
                print("right")
                control = "{}{}{}".format(control, 2, 0)

        # - unknown state - ignore
        else:
            print("Unused position at this time: x[{}], y[{}]".format(x_val, y_val))
            continue

        # send the control message over the xbee
        send_data(control)

        # print raw values
        print(control)
        time.sleep(0.2)
    except KeyboardInterrupt:
        break

# clean up, stop all activities
GPIO.cleanup()
