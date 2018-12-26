# 2-read-temp-humidity

Reads temperature and humidity from a DT11 temp/humidity sensor connected to a Raspbery
PI 3 B+ and prints the output to the terminal where the script has been run. Assumes the
following wiring connections (assumes a 10k built-in pull-up resistor - if this is not
present, ensure you wire a 10k resistor from the sensor DATA endpoint to the Raspberry PI
+5V source).

- GND to RasPi GND
- VCC to RasPi +5V
- DATA to RasPi GPIO4
- DATA to 10k pull-up resistor to RasPi +5V (only needed if no 10k built-in pull-up resistor
is present)

To run, execute the python script:

```bash
$ python main.py
```

You should see temperature and humidity values scroll by your screen every ~2 seconds, which
is the general refresh rate for the sensor.
