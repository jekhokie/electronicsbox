# 1-gui-led

Using the tkinter library, instantiates a GUI allowing a user to toggle an LED on/off
when connected to a Raspberry PI 3 B+ assuming the following wiring connections:

- LED NEG(-) to 1k Resistor to RasPi GND
- LED POS(+) to RasPi GPIO23

To run, execute the python script:

```bash
$ python main.py
```

You should then see a GUI pop up where you can control an LED on/off functionality.
