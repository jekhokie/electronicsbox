# 9-photocell

Prints out the value of a photocell connected to the Raspberry PI 3 B+. Since the Raspberry PI
3 does not have analog inputs, the circuit designed simulates analog translation. Assumes the following
wiring for the circuit:

- Photocell LEG1 to RasPi GPIO2 (PIN3)
- Photocell LEG2 to RasPi GND
- 1uF Capacitor POS to Photocell LEG1/RasPi GPIO2
- 1uF Capacitor NEG to RasPi GND

Note that the photoresistor used is a 4.2MM, 10K-100K Ohm Photocell, Part Number PDV-P9007 from
Advanced Photonix, Inc.

The way this circuit works is to first discharge the capacitor. Then, immediately upon starting to charge
the capacitor, increment a counter until the capacitor has reached approximately 75%, triggering the read
pin to flip to HIGH. Although fairly inaccurate as compared to digital devices, this rough estimate effort
can be used to trigger general thresholds for "dark" and "light" based on the pattern of repeated timings
for each.

To run, execute the python script:

```bash
$ python main.py
```

You should see the numeric value corresponding to approximately how long it took the capacitor to charge.
The number output is approximately 0.1ms increments, which is the rough time it takes for the `while`
loop in the code to execute for a pin read on the Raspberry PI.
