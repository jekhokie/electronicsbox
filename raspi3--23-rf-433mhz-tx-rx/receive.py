#!/usr/bin/env python3
#
# Receive data over a RF 433MHz receiver.
# See README.md for circuit diagram and connection expectations.
#

import argparse
import signal
import sys
import time
import logging
from rpi_rf import RFDevice

# configuration
RF_GPIO_PIN = 27

# handle SIGINT
# pylint: disable=unused-argument
def exithandler(signal, frame):
  rfdevice.cleanup()
  sys.exit(0)

# default logging format
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

# set up SIGINT handling
signal.signal(signal.SIGINT, exithandler)

# set up the RF device and configure for receive
rfdevice = RFDevice(RF_GPIO_PIN)
rfdevice.enable_rx()

# start listening for information
logging.info("Listening for codes on GPIO " + str(RF_GPIO_PIN))
timestamp = None
while True:
    currentTime = rfdevice.rx_code_timestamp
    # check if this is a new transmission data (de-bounce)
    if (currentTime != timestamp and (timestamp is None or currentTime - timestamp > 350000)):
        timestamp = rfdevice.rx_code_timestamp

        try:
            code = chr(rfdevice.rx_code)
            if code.isalnum():
                logging.info(chr(rfdevice.rx_code) + " [pulselength " + str(rfdevice.rx_pulselength) + ", protocol " + str(rfdevice.rx_proto) + "]")
        except:
            pass  # ignore invalid/unexpected characters

    time.sleep(0.01)

# release the RF receiver
rfdevice.cleanup()
