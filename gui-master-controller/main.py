#!/usr/bin/env python
#
# Functionality related to a full GUI command and control. Note that this functionality
# works with a Raspberry PI 3 B+ and although it may work for other versions, there
# are no guarantees. 
#
# The following wiring assumptions are present:
#   LED:
#     - LED NEG(-) to 1k Resistor to RasPi GND
#     - LED POS(+) to RasPi GPIO26
#
#   DT11 Temperature/Humidity Sensor (Assumes built-in 10k pull-up resistor):
#     - GND to RasPi GND
#     - VCC to RasPi +5V
#     - DATA to RasPi GPIO4
#     - DATA to 10k pull-up resistor to RasPi +5V (only needed if no 10k
#       built-in pull-up resistor is present)
#
# Prerequisites for Adafruit_DHT library:
#   sudo apt-get install git-core build-essential python-dev
#   git clone https://github.com/adafruit/Adafruit_python_DHT.git
#   cd Adafruit_Python_DHT/
#   sudo python setup.py install

import Tkinter as tk
import Adafruit_DHT
import time
from gpiozero import LED

WINDOW_WIDTH = 48
LED_PIN = 26
TEMP_PIN = 4

class App:

    def __init__(self, master):
        # initialize the sensor controls
        self.led = LED(LED_PIN)
        self.temp_sensor = Adafruit_DHT.DHT11
        self.temp_sensor_pin = TEMP_PIN

        # add a label
        main_label = tk.Label(master, text="Control All The Things!", height=3, width=WINDOW_WIDTH)
        main_label.grid(row=0, columnspan=4)

        # add the current time
        time_label = tk.Label(master, text="Current Time:", height=3)
        time_label.grid(row=1, column=0, columnspan=2)
        self.time_value = tk.Label(master, text="(Initializing...)", height=3)
        self.time_value.grid(row=1, column=1, columnspan=2)

        # add a button to control the LED
        self.led_control = tk.Button(master, text="Turn On LED", command=self.toggle_led, height=3, width=WINDOW_WIDTH)
        self.led_control.grid(row=2, columnspan=4)

        # add a label and value for the temperature
        self.temp_label = tk.Label(master, text="Temperature:", height=3)
        self.temp_label.grid(row=3, column=0, columnspan=1)
        self.temp_value = tk.Label(master, text="(Initializing...)", height=3)
        self.temp_value.grid(row=3, column=1, columnspan=1)

        # add a label and value for the humidity
        self.humid_label = tk.Label(master, text="Humidity:", height=3)
        self.humid_label.grid(row=3, column=2, columnspan=1)
        self.humid_value = tk.Label(master, text="(Initializing...)", height=3)
        self.humid_value.grid(row=3, column=3, columnspan=1)

        # add a button to exit
        exit_button = tk.Button(master, text="EXIT", command=self.quitApp, height=3, width=WINDOW_WIDTH)
        exit_button.grid(row=4, columnspan=4)

        # set a loop to update the time every 1 second
        master.after(1000, self.update_time)

        # set a loop to update the sensor data every 2 seconds
        master.after(2000, self.update_temp_humidity)

    # update the temperature and humidity values
    def update_temp_humidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.temp_sensor, self.temp_sensor_pin)
        self.temp_value["text"] = "{} F".format(((temperature/5)*9)+32)
        self.humid_value["text"] = "{} %".format(humidity)
        self.humid_value.after(2000, self.update_temp_humidity)

    # update the time in the GUI
    def update_time(self):
        cur_time = time.strftime("%H:%M:%S")
        self.time_value["text"] = cur_time
        self.time_value.after(1000, self.update_time)

    # control the LED on/off capability
    def toggle_led(self):
        if self.led.is_lit:
            print("Turning Off LED...")
            self.led.off()
        else:
            print("Turning On LED...")
            self.led.on()

    def quitApp(self):
        root.destroy()

# initialize the TK framework
root = tk.Tk()
root.title("LED Control")
app = App(root)
root.mainloop()
