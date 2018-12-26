# 0-blink-led

Will blink an LED on/off every 1 second assuming the following wiring from the Raspberry PI:

- LED NEG(-) to 1k Resistor to RasPi GND
- LED POS(+) to RasPi GPIO23

To run, execute the python script:

```bash
$ python main.py
```

You should then see the LED blink every 1 second on/off.
