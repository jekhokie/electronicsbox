# 14-joystick-adc-with-arduino-motor-shield

This tutorial is a piecing together of the following projects to formulate the basis for a robot and
associated robotic control:

1. 12-joystick-no-adc
2. 13-arduino-motor-shield-integration
3. 14-joystick-with-adc

The tutorial will use an analog joystick at a base station to remote control (using XBee modules) a
robot with DC motors controlled by a receiver XBee into a Raspberry Pi controlling the motors through
an Arduino Motor shield. The robot will have its own power sources (battery and USB power from cell
phone charger with 5V power regulator for quality 5V signal), and the base station will consist of the
joystick, MCP3008 ADC, and Raspberry Pi plugged into a USB power source.

TODO:
- encoding description for motor control messages
- wiring description
- SPI Enablement
- I2C Enablement
- Virtualenv/python 3
- requirements.txt/pip install
- usage
- circuit diagram
