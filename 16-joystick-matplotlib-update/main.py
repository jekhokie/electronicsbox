#!/usr/bin/env python
#
# Script to plot an analog joystick value on a graph for the purposes of plotting
# a normalized value according to an assumption that motors will operate within a
# range of 0-255 in either forward or reverse direction.

from __future__ import division
import datetime as dt
### WORKAROUND: FOR MAC OSX ISSUES ###
import matplotlib
matplotlib.use('TkAgg')
### ENDWORKAROUND ###
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random

# configurations for tuning the script
MIN_X = 0               # analog sensor x-axis minimum value
MAX_X = 65472           # analog sensor x-axis maximum value
MIN_Y = 0               # analog sensor y-axis minimum value
MAX_Y = 65472           # analog sensor y-axis maximum value
STABLE_X_SIZE = 5000    # 'quiet' area X size/range
STABLE_Y_SIZE = 5000    # 'quiet' area Y size/range
SENSOR_READ_MS = 500    # sleep time (in ms) between sensor reads
MOTOR_MIN = 0           # minimum value possible for motor control
MOTOR_MAX = 255         # maximum value possible for motor control

# create plot figure with boundaries
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, MAX_X)
ax.set_ylim(0, MAX_Y)

# scale the analog sensor read to a value a motor expects
def scale_to_motor(value, min_value, max_value):
    new_value = (MOTOR_MAX - MOTOR_MIN) / (max_value - min_value) * (value - min_value) + MOTOR_MIN
    return int(new_value)

# main update loop
def update_graph(i, xs, ys, x_start, x_size, y_start, y_size):
    '''
    Dynamically update plot with sensor value and dashed rectangle
    indicating the "quiet zone" (x_start, x_size, y_start, y_size)
    '''

    ## DEBUG CODE: REPLACE WITH SENSOR READ VALUES ##
    x_value = random.randint(-MAX_X, MAX_X)
    y_value = random.randint(-MAX_Y, MAX_Y)
    #################################################

    # convert to motor-expected scale
    scaled_x = scale_to_motor(x_value, MIN_X, MAX_X)
    scaled_y = scale_to_motor(y_value, MIN_Y, MAX_Y)

    # move axes to center like cross-hair,
    # with negative to positive motor values,
    # and disable autoscale, then plot value
    ax.clear()
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_xlim(-MOTOR_MAX, MOTOR_MAX)
    ax.set_ylim(-MOTOR_MAX, MOTOR_MAX)
    ax.set_autoscale_on(False)
    ax.plot(scaled_x, scaled_y, "bs")
    ax.annotate(str("{}, {}".format(scaled_x, scaled_y)), (scaled_x + 5.0, scaled_y + 5.0))

    # plot the "quiet" zone where no movement is expected
    quiet_zone = patches.Rectangle((x_start, y_start), x_size, y_size,
                                   linestyle='--', linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(quiet_zone)

# calculate the center/resting position of the joystick analog value
mid_x = (MAX_X - MIN_X) / 2.0
mid_y = (MAX_Y - MIN_Y) / 2.0

# calculate the scaled components for the quiet zone for the joystick
stable_x_size = scale_to_motor(STABLE_X_SIZE, MIN_X, MAX_X)
stable_y_size = scale_to_motor(STABLE_Y_SIZE, MIN_Y, MAX_Y)
stable_x_start = -(stable_x_size / 2.0)
stable_y_start = -(stable_y_size / 2.0)

# dynamic update on interval
ani = animation.FuncAnimation(fig, update_graph, fargs=(0, 0, stable_x_start, stable_x_size, stable_y_start, stable_y_size),
                              interval=SENSOR_READ_MS)
plt.show()
