#!/usr/bin/env python
#
# Read of a DT11 Temperature/Humidity sensor with a Raspberry PI 3 B+.
# Assumes the sensor has a built-in 10k pull-up resistor, but if not,
# ensure you add a 10k resistor from DATA to +5V on the Raspberry PI.
# Assumes the following wiring:
#
# - GND to RasPi GND
# - VCC to RasPi +5V
# - DATA to RasPi GPIO4
# - DATA to 10k pull-up resistor to RasPi +5V (only needed if no 10k
#   built-in pull-up resistor is present)
#
# Prerequisites for Adafruit_DHT library:
#   sudo apt-get install git-core build-essential python-dev
#   git clone https://github.com/adafruit/Adafruit_python_DHT.git
#   cd Adafruit_Python_DHT/
#   sudo python setup.py install

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
sensor_pin = 4

# read and print temperature/humidity every 2 seconds (default for read_retry)
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    print("Temp: {0:0.1f} F | Humidity: {1:0.1f} %".format(((temperature/5)*9)+35, humidity))
