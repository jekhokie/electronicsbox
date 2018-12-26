#!/usr/bin/env python
#
# Control of an LED through a GUI driven by Tkinter. Works for a Raspberry PI 3 B+.
# Assumes the following wiring:
#
# - LED NEG(-) to 1k Resistor to RasPi GND
# - LED POS(+) to RasPi GPIO26

import Tkinter as tk
import RPi.GPIO as GPIO
from gpiozero import LED

# set the GPIO pin for the LED
LED_PIN = 26

# set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class App:

    def __init__(self, master):
        # initialize the LED controls
        self.led = LED(LED_PIN)

        # add a label
        main_label = tk.Label(master, text="Control LEDs")
        main_label.grid(row=0)

        # add a button to control the LED
        self.led_control = tk.Button(master, text="Turn On LED", command=self.toggle_led, height=1, width=24)
        self.led_control.grid(row=1)

        # add a button to exit
        exit_button = tk.Button(master, text="EXIT", command=self.quit_app, height=1, width=24)
        exit_button.grid(row=2)

    # control the LED on/off capability
    def toggle_led(self):
        if self.led.is_lit:
            self.led.off()
            self.led_control["text"] = "Turn On LED"
        else:
            self.led.on()
            self.led_control["text"] = "Turn Off LED"

    def quit_app(self):
        root.destroy()

# initialize the TK framework
root = tk.Tk()
root.title("LED Control")
app = App(root)
root.mainloop()
