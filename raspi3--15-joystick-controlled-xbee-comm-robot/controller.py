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

from __future__ import division
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

# thresholds for joystick and normalization
MIN_X = 0               # analog sensor x-axis minimum value
MAX_X = 65472           # analog sensor x-axis maximum value
MIN_Y = 0               # analog sensor y-axis minimum value
MAX_Y = 65472           # analog sensor y-axis maximum value
STABLE_X_SIZE = 5000    # 'dead' area X size/range
STABLE_Y_SIZE = 5000    # 'dead' area Y size/range
SENSOR_READ_MS = 100    # sleep time (in ms) between sensor reads
MOTOR_MIN = -255        # minimum value possible for motor control
MOTOR_MAX = 255         # maximum value possible for motor control
#MIN_THRESHOLD = 30000
#MAX_THRESHOLD = 40000

# configure pins as appropriate
MCP_CS_PIN = board.D5       # MCP3008 CS
MCP_MISO_PIN = board.MISO   # MCP3008 MISO
MCP_MOSI_PIN = board.MOSI   # MCP3008 MOSI
MCP_SCK_PIN = board.SCK     # MCP3008 SCLK
JOY_X_MCP_IN = MCP.P0       # MCP3008 Joystick X-Axis Input (CH0)
JOY_Y_MCP_IN = MCP.P1       # MCP3008 Joystick Y-Axis Input (CH1)
LIGHT_PIN = 12              # pin for on/off for under-carriage lighting
BUTTON_PIN = 13             # joystick select for horn/buzzer
SERIAL_PORT = "/dev/ttyS0"  # serial port for xbee usage
BAUD_RATE = 9600            # baud rate for xbee communication

# ADC setup - create SPI bus, chip select, and resulting mcp object
spi = busio.SPI(clock=MCP_SCK_PIN, MISO=MCP_MISO_PIN, MOSI=MCP_MOSI_PIN)
cs = digitalio.DigitalInOut(MCP_CS_PIN)
mcp = MCP.MCP3008(spi, cs)

# create analog inputs for the joystick on the MCP3008,
# and set up joystick horn and undercarriage light buttons
x_chan = AnalogIn(mcp, JOY_X_MCP_IN)
y_chan = AnalogIn(mcp, JOY_Y_MCP_IN)
GPIO.setup(LIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure the xbee
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, escaped=False)

def send_data(data):
    '''
    Send data from a transmitting XBee to a receiving XBee device.
    '''
    xbee.send("tx", dest_addr=b'\x00\x00', data=bytes("{}".format(data), 'utf-8'))

def scale_to_motor(value, min_value, max_value):
    '''
    Scale the incoming value to the range of the min and max for the
    motors, using the following formula to normalize in [a, b] (for
    instance, [-255, 255] for reverse to forward motor control):
                             (x - min_x)
        x_norm = (b - a) * --------------- + a
                           (max_x - min_x)
    '''

    new_value = (MOTOR_MAX - MOTOR_MIN) * ( (value - min_value) / (max_value - min_value) ) + MOTOR_MIN
    return int(new_value)

# calculate the scaled components for the dead zone for the joystick
stable_x_size = scale_to_motor(STABLE_X_SIZE, MIN_X, MAX_X) / 2
stable_y_size = scale_to_motor(STABLE_Y_SIZE, MIN_Y, MAX_Y) / 2
stable_x_start = -(stable_x_size / 2.0)
stable_y_start = -(stable_y_size / 2.0)

# main execution loop
# maintain the state of the light since we are using a momentary button
# to enable/disable teh light
light_state = 0
last_light_button_state = False
while True:
    try:
        # perform one-time lookup of values for joystick, buzzer button, and light button
        x_val = x_chan.value
        y_val = y_chan.value
        buzzer = GPIO.input(BUTTON_PIN)
        light = GPIO.input(LIGHT_PIN)

        # convert joystick to motor-expected scale
        scaled_x = scale_to_motor(x_val, MIN_X, MAX_X)
        scaled_y = scale_to_motor(y_val, MIN_Y, MAX_Y)

        # calculate motor control on/off based on following scheme:
        #       <LIGHT><BUZZER><LEFT_MOTOR><RIGHT_MOTOR>
        # where the LIGHT is either 0 or 1,
        # BUZZER is either 0 or 1 and each motor
        # value is either a 0 (reverse), 1 (stop), or 2 (forward)
        # first, the light
        if light == False and last_light_button_state == True:
            if light_state == 0:
                light_state = 1
            else:
                light_state = 0

        control = "{}".format(light_state)
        last_light_button_state = light

        # next, the buzzer
        if buzzer == False:
            control = "{}{}".format(control, 1)
        else:
            control = "{}{}".format(control, 0)

        # next, the motors
        # - brake: both off (in dead zone)
        if scaled_x > (stable_x_start + stable_x_size) and scaled_x < stable_x_start and scaled_y > (stable_y_start + stable_y_size) and scaled_y < stable_y_start:
            control = "{}{}{:03d}{}{:03d}".format(control, 1, 0, 1, 0)
        else:
            # default to forward, and switch to reverse if necessary
            l_dir = r_dir = 2
            if scaled_y < 0:
                l_dir = r_dir = 0

            # configure left/right motor speeds based on direction of joystick
            # x in dead zone is straight ahead (assume this)
            # x < dead zone is left-hand turn
            # x > dead zone is right-hand turn
            scaled_y = abs(scaled_y)
            if scaled_x > (stable_x_start + stable_x_size) and scaled_x < stable_x_start:
                # - straight ahead
                l_speed = scaled_y
                r_speed = scaled_y
            if scaled_x < (stable_x_start + stable_x_size):
                # - left-hand turn
                l_speed = (1 - (scaled_x / MOTOR_MIN)) * scaled_y
                r_speed = scaled_y
            elif scaled_x > stable_x_start:
                # - right-hand turn
                l_speed = scaled_y
                r_speed = (1 - (scaled_x / MOTOR_MAX)) * scaled_y

            # update control logic
            control = "{}{}{:03d}{}{:03d}".format(control, l_dir, int(l_speed), r_dir, int(r_speed))

        # send the control message over the xbee
        send_data(control)

        # print raw values
        print(control)
        time.sleep(0.2)
    except KeyboardInterrupt:
        break

# clean up, stop all activities
GPIO.cleanup()
