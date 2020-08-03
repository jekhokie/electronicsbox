#!/usr/bin/env python3
#
# Print Raspberry Pi system information on an OLED display.
# See README.md for circuit diagram and connection expectations.
#

import time
import subprocess
import board
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
 
# i2c address, width, and height of the OLED
OLED_ADDR = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 64
   
# initialize i2c and bus
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)
     
# clear display
oled.fill(0)
oled.show()
      
# create blank image for drawing, get drawing object, and load default fonts
image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
 
try:
    while True:
        # draw a black filled box to clear the image
        draw.rectangle((0, 0, OLED_WIDTH, OLED_HEIGHT), outline=0, fill=0)
     
        # execute shell commands for collecting system information for display
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # draw system information to screen
        draw.text((0, 0), "IP: " + IP, font=font, fill=255)
        draw.text((0, 8), CPU, font=font, fill=255)
        draw.text((0, 16), MemUsage, font=font, fill=255)
        draw.text((0, 25), Disk, font=font, fill=255)

        # display image
        oled.image(image)
        oled.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    # handle CTRL-C or other termination SIGINT
    print("SIGINT detected - releasing screen")
    oled.fill(0)
    oled.show()
    exit(0)
