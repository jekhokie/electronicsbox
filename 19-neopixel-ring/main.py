#!/usr/bin/env python
#
# Several displays on a NeoPixel ring with 16x LEDs. Assumes the following wiring connections,
# and a Raspberry Pi Zero WH is used as the compute instance:
# (for testing):
#
# - NeoPixel Ring DIN to RasPi GPIO18
# - NeoPixel Ring POS(+) to RasPi POS +5V
# - NeoPixel Ring NEG(-) to RasPi GND
#
# Note that this code is brute-force and not DRY/needs improvement - the focus is on functionality
# over form.

import board
import neopixel
import time
import random
from signal import signal, SIGINT

# NUM_PIXELS: number of LEDs on the NeoPixel
# TRIALS: how many times to run each method
# PIN: Raspberry Pi pin to use (should likely leave as D18)
# RAND_COLORS: set of random RGBW colors
NUM_PIXELS = 16
TRIALS = 3
PIN = board.D18
RAND_COLORS = [
    (255, 0, 0, 0),
    (0, 255, 0, 0),
    (0, 0, 255, 0),
    (128, 128, 0, 0),
    (0, 128, 128, 0),
    (128, 0, 128, 0),
    (255, 255, 0, 0),
    (255, 0, 255, 0),
    (0, 255, 255, 0)
]

# initialize the LEDs
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False, pixel_order=neopixel.RGBW)

def resetPixels(signal_received, frame):
    '''Intercept a SIGINT/CTRL-C and reset the LED strip'''
    pixels.deinit()
    exit(0)

def randomChaser():
    '''Random LED colors chasing each other in a circle'''
    for i in range(0, NUM_PIXELS):
        color = RAND_COLORS[random.randint(0, len(RAND_COLORS)-1)]
        if i == 0:
            pixels[NUM_PIXELS-1] = color
        else:
            pixels[i-1] = color

        pixels[i] = color

        if i == NUM_PIXELS-1:
            pixels[0] = color
        else:
            pixels[i+1] = color

        pixels.show()
        time.sleep(0.05)
        pixels.fill((0, 0, 0, 0))
        pixels.show()

def greenGlower():
    '''All LEDs lighting up and fading like an alert'''
    for i in range(0, 255, 5):
        pixels.fill((i, 0, 0, 0))
        pixels.show()
    for i in reversed(range(0, 255, 5)):
        pixels.fill((i, 0, 0, 0))
        pixels.show()

def upDownChase():
    '''Perform a side-by-side dual LED chase up/down the pixel ring'''
    for i in range(0, int(NUM_PIXELS/2)):
        pixels[i] = pixels[NUM_PIXELS-1-i] = (0, 255, 0, 0)
        pixels.show()
        time.sleep(0.05)
        pixels.fill((0, 0, 0, 0))
    for i in reversed(range(0, int(NUM_PIXELS/2))):
        pixels[i] = pixels[NUM_PIXELS-1-i] = (0, 255, 0, 0)
        pixels.show()
        time.sleep(0.05)
        pixels.fill((0, 0, 0, 0))

def randomBlinking():
    '''Blink random colors all over the ring'''
    for i in random.sample(range(0, NUM_PIXELS), NUM_PIXELS):
        color = RAND_COLORS[random.randint(0, len(RAND_COLORS)-1)]
        pixels[i] = color
        pixels.show()
        time.sleep(0.05)

if __name__ == '__main__':
    signal(SIGINT, resetPixels)

    # cycle through each capability 3 times
    while True:
        # random LED colors chasing in a circle
        for i in range(TRIALS):
            randomChaser()

        # increase/decrease intensity glowing like an
        # alert sequence
        for i in range(TRIALS):
            greenGlower()

        # perform a parallel up/down chase visualization
        for i in range(TRIALS):
            upDownChase()

        # random LED colors all over the ring
        for i in range(TRIALS):
            randomBlinking()
