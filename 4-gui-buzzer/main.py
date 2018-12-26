#!/usr/bin/env python
#
# Control of an Active Buzzer through a GUI driven by Tkinter. Works for a Raspberry PI
# 3 B+. Assumes the following wiring connections, including an LED to indicate on/off
# (for testing):
#
# - Buzzer POS(+) to RasPi GPIO18
# - Buzzer NEG(-) to RasPi GND
# - LED POS(+) to RasPi GPIO18
# - LED NEG(-) to 1k Ohm Resistor to RasPi GND

import Tkinter as tk
import RPi.GPIO as GPIO

# set the GPIO pin
BUZZER_PIN = 18

# set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class App:

    def __init__(self, master):
        # initialize the Buzzer controls
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        # add a label
        main_label = tk.Label(master, text="Control Buzzer")
        main_label.grid(row=0)

        # add a button to control the Buzzer
        self.buzzer_control = tk.Button(master, text="Turn On Buzzer", command=self.toggle_buzzer, height=1, width=24)
        self.buzzer_control.grid(row=1)

        # add a button to exit
        exit_button = tk.Button(master, text="EXIT", command=self.quit_app, height=1, width=24)
        exit_button.grid(row=2)

    # control the Buzzer on/off capability
    def toggle_buzzer(self):
        if (GPIO.input(BUZZER_PIN) == 1):
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            self.buzzer_control["text"] = "Turn On Buzzer"
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            self.buzzer_control["text"] = "Turn Off Buzzer"

    def quit_app(self):
        GPIO.cleanup()
        root.destroy()

# initialize the TK framework
root = tk.Tk()
root.title("Buzzer Control")
app = App(root)
root.mainloop()
