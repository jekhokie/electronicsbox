#!/usr/bin/env python
#
# Controller for robot actions.

import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

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

# create SPI bus, chip select, and resulting mcp object
spi = busio.SPI(clock=MCP_SCK_PIN, MISO=MCP_MISO_PIN, MOSI=MCP_MOSI_PIN)
cs = digitalio.DigitalInOut(MCP_CS_PIN)
mcp = MCP.MCP3008(spi, cs)

# create analog inputs for the joystick on the MCP3008
x_chan = AnalogIn(mcp, JOY_X_MCP_IN)
y_chan = AnalogIn(mcp, JOY_Y_MCP_IN)

# set up our select button on the joystick for the buzzer/horn
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

### DEBUGMOVE ###
HORN_PIN = 19
GPIO.setup(HORN_PIN, GPIO.OUT)

# default I2C communication - all Arduino Motor Shields ship with
# address 0x60 as referenceable I2C address
mh = Adafruit_MotorHAT(addr=0x60)
left_motor = mh.getMotor(1)
#right_motor = mh.getMotor(2)
### ENDDEBUGMOVE ###

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

        ### DEBUGMOVE ###
        if len(control) != 3:
            print("Did not get valid control message ({}) - ignoring".format(control))
        else:
            # horn control
            if control[0] == "1":
                GPIO.output(HORN_PIN, GPIO.HIGH)
            else:
                GPIO.output(HORN_PIN, GPIO.LOW)

            # motor movement for left motor and right motor control
            lmc = control[1]
            rmc = control[2]

            if lmc == "0":
                left_motor.run(Adafruit_MotorHAT.BACKWARD)
                left_motor.setSpeed(255)
            elif lmc == "1":
                left_motor.run(Adafruit_MotorHAT.RELEASE)
                left_motor.setSpeed(0)
            elif lmc == "2":
                left_motor.run(Adafruit_MotorHAT.FORWARD)
                left_motor.setSpeed(255)
            else:
                print("Invalid entry for left motor control: {}".format(lmc))
        ### ENDDEBUGMOVE ###

        # print raw values
        print(control)
        time.sleep(0.2)
    except KeyboardInterrupt:
        break

# clean up, stop all activities
GPIO.cleanup()

### DEBUGMOVE ###
mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
### ENDDEBUGMOVE ###
