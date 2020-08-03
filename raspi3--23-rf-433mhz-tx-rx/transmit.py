#!/usr/bin/env python3
#
# Transmit data over a RF 433MHz transmitter.
# See README.md for circuit diagram and connection expectations.
#

import argparse
import logging
from rpi_rf import RFDevice

# configuration
RF_GPIO_PIN = 17
RF_PULSE_LEN = 350
RF_PROTOCOL = 1

# default logging format
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

# set up the RF device and configure for transmission
rfdevice = RFDevice(RF_GPIO_PIN)
rfdevice.enable_tx()

# transmit 5 characters, and then clean up
for x in ['A', 'B', 'C', 'D', 'E']:
    logging.info(str(x) + " [protocol: " + str(RF_PROTOCOL) + ", pulselength: " + str(RF_PULSE_LEN) + "]")
    rfdevice.tx_code(ord(x), RF_PROTOCOL, RF_PULSE_LEN)

# release the RF transmitter
rfdevice.cleanup()
