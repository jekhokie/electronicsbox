# 16-joystick-matplotlib-update

Plots values for an analog Joystick (using an Analog 2-axis Thumb Joystick from Adafruit, specs
located [here](http://adafru.it/512)) connected to the Raspberry Pi 3 B+ with an MCP3008 analog to
digital converter (ADC). This tutorial is an extension of the 14-joystick-with-adc tutorial in that it
plots the analog value of the Joystick output *normalized* against what the DC motor library expects for
a value of 0-255 to help with charting the next course of action for analog DC TT motor control with
variable speed and direction. The assumption for wiring is teh same as in the 14-joystick-with-adc
tutorial and will not be repeated here. Follow the steps in the 14-joystick-with-adc tutorial for wiring
and Raspberry Pi configuration (as well as the `virtualenv` creation and library installation steps).

## Prerequisites

This script on a Raspberry Pi requires the `libatlas-base-dev` package to be installed to avoid receiving
`numpy` errors. First, install the package:

```bash
$ sudo apt-get install libatlas-base-dev
```

## Execution

Once wiring is complete, virtualenv is created, and libraries are installed according to the steps in
14-joystick-with-adc, you can execute the tutorial like so:

```bash
$ python main.py
```

Once the script kicks off, you should see a graph showing the analog values for the joystick normalized
against a 0-255 value set on the graph to be used for driving motor control.
