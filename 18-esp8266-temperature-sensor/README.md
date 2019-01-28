# 18-esp8266-temperature-sensor

This tutorial uses an [ESP8266-01](https://en.wikipedia.org/wiki/ESP8266) with a DHT22 temperature
sensor to send temperature and humidity data to a remote endpoint (statsd on the Raspberry Pi).

## Details

Please see [this post](https://jekhokie.github.io/esp8266/wifi/arduino/electronics/2019/01/25/esp8266-temp-sensor.html)
for details including initial programming, blink LED tutorial, and finally, the actual DHT22 sensor
hookup instructions.

## Additional Information

Throughout the tutorial several other commands were found to be useful - here is a list of commands that
are for good reference (possibly useful in the future):

### Links

- [ESP8266 Community Forum](https://www.esp8266.com/)
- [ESP8266-01 Deep Sleep Mod](https://www.instructables.com/id/Enable-DeepSleep-on-an-ESP8266-01/)
- [EspressIf AT Firmware](https://www.espressif.com/en/products/hardware/esp8266ex/resources)
- [ElectroDragon AT Firmware](https://www.electrodragon.com/w/File:AT_V1.1_on_ESP8266_NONOS_SDK_V1.5.4.zip)
- [MicroPython firmware](https://docs.micropython.org/en/latest/esp8266/tutorial/index.html)
- [ESP8266 Board Reference for Arduino IDE](http://arduino.esp8266.com/stable/package_esp8266com_index.json)
- [FTDI USB to Serial Board](https://www.sparkfun.com/products/9873)
- [uPyCraft IDE](https://github.com/DFRobot/uPyCraft)
- [Flash Chip Vendor List](https://review.coreboot.org/cgit/flashrom.git/tree/flashchips.h)

### Commands

```bash
# install esptool (used for flashing from command line)
$ pip install esptool

# get information about flash, including vendor and size
$ esptool.py --port /dev/ttyUSB0 flash_id

# erase the entire flash memory on the ESP8266 connected to /dev/ttyUSB0
$ esptool.py --port /dev/ttyUSB0 erase_flash

# upload firmware pieces to respective address locations (need to press reset before each load):
- esptool.py --port /dev/ttyUSB0 write_flash --flash_size detect 0xfc00 esp_init_data_default_v08.bin
- esptool.py --port /dev/ttyUSB0 write_flash --flash_size detect 0xfe00 blank.bin
- esptool.py --port /dev/ttyUSB0 write_flash --flash_size detect 0x0000 boot_v1.7.bin
- esptool.py --port /dev/ttyUSB0 write_flash --flash_size detect 0x0100 at/1024+1024/user1.2048.new.5.bin

# upload all firmware pieces in one command without needing to reset between commands:
$ esptool.py --port /dev/ttyUSB0 write_flash --flash_size detect \\
    0xfc00 esp_init_data_default_v08.bin \\
    0xfe00 blank.bin \\
    0x0000 boot_v1.7.bin \\
    0x0100 at/1024+1024/user1.2048.new.5.bin
```
