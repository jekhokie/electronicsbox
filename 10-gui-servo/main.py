#!/usr/bin/env python
#
# Controls a servo (through a GUI) motor connected to a Raspberry Pi 3 B+ with an
# external/separate +5V power supply powering the servo. Assumes the following wiring:
# 
# - Servo SIG/PWM to 1k Ohm Resistor to RasPi GPIO27 (PIN13)
# - Servo VCC to +5V Power Supply POS(+)
# - Servo GND to RasPi GND/+5V Power Supply GND (Joined)
# - RasPi GND to +5V Power Supply GND
 
import Tkinter as tk
import RPi.GPIO as GPIO
import time

# which Raspberry PI pin to use for the servo
SERVO_PIN = 27

# some UI settings
WINDOW_WIDTH = 48

# use BCM pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# configure PWM pin
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 100)
pwm.start(5)

class App:

    def __init__(self, master):
        # initialize the LED controls
        scale_label = tk.Label(master, text="Control Servo", height=3, width=WINDOW_WIDTH)
        scale_label.grid(row=0)
        scale_control = tk.Scale(master, from_=0, to=180, orient=tk.HORIZONTAL, command=self.update_servo, width=WINDOW_WIDTH)
        scale_control.grid(row=1)

        # add a button to exit
        exit_button = tk.Button(master, text="EXIT", command=self.quit_app, height=3, width=WINDOW_WIDTH)
        exit_button.grid(row=2)

    # update the servo when the servo control changes
    def update_servo(self, angle):
        d = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(d)

    # quit and clean up after ourselves
    def quit_app(self):
        GPIO.cleanup()
        root.destroy()

# initialize the TK framework
root = tk.Tk()
root.title("Servo Control")
app = App(root)
root.mainloop()
