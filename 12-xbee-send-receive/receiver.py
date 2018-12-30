#!/usr/bin/env python3
#
# Acts as a receiver of data from a sending XBee module, and controls
# LEDs (up, down, left, right) associated with the codes sent by the trasmitter.
# See README for additional information.
#
# **NOTE: REQUIRES PYTHON 3**

import serial, time
from xbee import XBee

# which Raspberry PI pin to use for the servo
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# handler for whenever data is received from transmitters
# operates asynchronously
def receive_data(data):
    print("Packet: {}".format(data))
    print("Data: {}".format(data['rf_data']))

# configure the xbee and enable asynchronous mode
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, callback=receive_data, escaped=False)

while True:
    try:
        # operate in async mode where all messages will go to handler
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

# close the serial port
xbee.halt()
ser.close()
