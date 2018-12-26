#!/usr/bin/env python
#
# Functionality related to a full GUI command and control. Note that this functionality
# works with a Raspberry PI 3 B+ and although it may work for other versions, there
# are no guarantees. 
#
# The following wiring assumptions are present:
#   LED:
#     - LED NEG(-) to 1k Resistor to RasPi GND
#     - LED POS(+) to RasPi GPIO23
#
#   DT11 Temperature/Humidity Sensor (Assumes built-in 10k pull-up resistor):
#     - GND to RasPi GND
#     - VCC to RasPi +5V
#     - DATA to RasPi GPIO4
#     - DATA to 10k pull-up resistor to RasPi +5V (only needed if no 10k
#       built-in pull-up resistor is present)
#
#   Push-Button:
#     - Button END1 to RasPi GND
#     - Button END2 to RasPi GPIO24
#
#   Active Buzzer:
#     - Buzzer POS(+) to RasPi GPIO18
#     - Buzzer NEG(-) to RasPi GND
#     - LED POS(+) to RasPi GPIO18
#     - LED NEG(-) to 1k Ohm Resistor to RasPi GND
#
#   2-Way, 3-Wire Switch:
#     - SWITCH MIDDLE PIN to RasPi +3.3V
#     - SWITCH LEFT PIN to RasPi GPIO17
#     - SWITCH RIGHT PIN to RasPi GPIO27
#     - SWITCH LEFT PIN to 10k Ohm Resistor to RasPi GND (parallel)
#     - SWITCH RIGHT PIN to 10k Ohm Resistor to RasPi GND (parallel)
#
# Prerequisites for Adafruit_DHT library:
#   sudo apt-get install git-core build-essential python-dev
#   git clone https://github.com/adafruit/Adafruit_python_DHT.git
#   cd Adafruit_Python_DHT/
#   sudo python setup.py install

import Adafruit_DHT
import time
import Tkinter as tk
import RPi.GPIO as GPIO
from gpiozero import LED

# set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GUI Defaults
WINDOW_WIDTH = 48

# sensor pin defaults
TEMP_PIN          = 4
SWITCH_STATE1_PIN = 17
BUZZER_PIN        = 18
LED_PIN           = 23
BUTTON_PIN        = 24
SWITCH_STATE2_PIN = 27

# refresh defaults
TIME_UPDATE_FREQ = 1000
TEMP_UPDATE_FREQ = 5000
BUTTON_UPDATE_FREQ = 1000
SWITCH_UPDATE_FREQ = 1000

class App:

    def __init__(self, master):
        # initialize the sensor controls
        # - LED
        self.led = LED(LED_PIN)
        # - temp/humidity sensor
        self.temp_sensor = Adafruit_DHT.DHT11
        self.temp_sensor_pin = TEMP_PIN
        # - button
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # - buzzer
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        # - 2-way switch
        GPIO.setup(SWITCH_STATE1_PIN, GPIO.IN)
        GPIO.setup(SWITCH_STATE2_PIN, GPIO.IN)

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
        temp_label = tk.Label(master, text="Temperature:", height=3)
        temp_label.grid(row=3, column=0, columnspan=1)
        self.temp_value = tk.Label(master, text="(Initializing...)", height=3)
        self.temp_value.grid(row=3, column=1, columnspan=1)

        # add a label and value for the humidity
        humid_label = tk.Label(master, text="Humidity:", height=3)
        humid_label.grid(row=3, column=2, columnspan=1)
        self.humid_value = tk.Label(master, text="(Initializing...)", height=3)
        self.humid_value.grid(row=3, column=3, columnspan=1)

        # add a label and value for the button status
        button_label = tk.Label(master, text="Button:", height=3)
        button_label.grid(row=4, column=0, columnspan=1)
        self.button_value = tk.Label(master, text="(Initializing...)", height=3)
        self.button_value.grid(row=4, column=1, columnspan=1)

        # add a label and value for the 2-way switch status
        switch_label = tk.Label(master, text="Switch:", height=3)
        switch_label.grid(row=4, column=2, columnspan=1)
        self.switch_value = tk.Label(master, text="(Initializing...)", height=3)
        self.switch_value.grid(row=4, column=3, columnspan=1)

        # add a button to control the Active Buzzer
        self.buzzer_control = tk.Button(master, text="Turn On Buzzer", command=self.toggle_buzzer, height=3, width=WINDOW_WIDTH)
        self.buzzer_control.grid(row=5, columnspan=4)

        # add a button to exit
        exit_button = tk.Button(master, text="EXIT", command=self.quitApp, height=3, width=WINDOW_WIDTH)
        exit_button.grid(row=10, columnspan=4)

        # set a loop to update the time every 1 second
        master.after(TIME_UPDATE_FREQ, self.update_time)

        # set a loop to update the sensor data every 2 seconds
        master.after(TEMP_UPDATE_FREQ, self.update_temp_humidity)

        # set a loop to update the button data every 1 seconds
        master.after(BUTTON_UPDATE_FREQ, self.update_button_status)

        # set a loop to update the 2-way switch data every 1 seconds
        master.after(SWITCH_UPDATE_FREQ, self.update_switch_status)

    # update the temperature and humidity values
    def update_temp_humidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.temp_sensor, self.temp_sensor_pin)
        self.temp_value["text"] = "{} F".format(((temperature/5)*9)+32)
        self.humid_value["text"] = "{} %".format(humidity)
        self.humid_value.after(TEMP_UPDATE_FREQ, self.update_temp_humidity)

    # update the time in the GUI
    def update_time(self):
        cur_time = time.strftime("%H:%M:%S")
        self.time_value["text"] = cur_time
        self.time_value.after(TIME_UPDATE_FREQ, self.update_time)

    # determine if the button is pressed and update the GUI
    def update_button_status(self):
        button_status = "Not Pressed"
        input_state = GPIO.input(BUTTON_PIN)

        if input_state == False:
            button_status = "Pressed"

        self.button_value["text"] = button_status
        self.button_value.after(BUTTON_UPDATE_FREQ, self.update_button_status)

    # update the 2-way switch position
    def update_switch_status(self):
        switch_status = "UNK"

        if (GPIO.input(SWITCH_STATE1_PIN) == 1):
            switch_status = "LEFT"
        elif (GPIO.input(SWITCH_STATE2_PIN) == 1):
            switch_status = "RIGHT"

        self.switch_value["text"] = switch_status
        self.switch_value.after(SWITCH_UPDATE_FREQ, self.update_switch_status)

    # control the LED on/off capability
    def toggle_led(self):
        if self.led.is_lit:
            self.led.off()
            self.led_control["text"] = "Turn On LED"
        else:
            self.led.on()
            self.led_control["text"] = "Turn Off LED"

    # control the Active Buzzer on/off capability
    def toggle_buzzer(self):
        if (GPIO.input(BUZZER_PIN) == 1):
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            self.buzzer_control["text"] = "Turn On Buzzer"
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            self.buzzer_control["text"] = "Turn Off Buzzer"

    # handle quitting application
    def quitApp(self):
        root.destroy()

# initialize the TK framework
try:
    root = tk.Tk()
    root.title("Full Control")
    app = App(root)
    root.mainloop()
except KeyboardInterrupt:
    print("Exiting...")
