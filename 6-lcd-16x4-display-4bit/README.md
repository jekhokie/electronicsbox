# 6-lcd-16x4-display-4bit

Writes information to a 16x4 LCD display wired and programmed using 4-bit configuration connected
to a Raspberry PI 3 B+. Assumes the following setup:

- LCD PIN1 (VSS) to RasPi GND
- LCD PIN2 (VDD) to RasPi +5V
- LCD PIN3 (VO) to POT1 CENTER PIN
- LCD PIN4 (RS) to RasPi GPIO26 (BCM PIN37)
- LCD PIN5 (RW) to RasPi GND
- LCD PIN6 (E) to RasPi GPIO19 (BCM PIN35)
- LCD PIN7-PIN10 (NOT USED)
- LCD PIN11 (D4) to RasPi GPIO13 (BCM PIN33)
- LCD PIN12 (D5) to RasPi GPIO6 (BCM PIN31)
- LCD PIN13 (D6) to RasPi GPIO5 (BCM PIN29)
- LCD PIN14 (D7) to RasPi GPIO11 (BCM PIN23)
- LCD PIN15 (A) to POT2 RIGHT PIN
- LCD PIN16 (K) to RasPi GND
- POT1 RIGHT PIN to RasPi GND
- POT2 CENTER PIN to RasPi +5V

First, prerequisites must be installed:

```bash
$ pip install -r requirements.txt
```

Next, to run, execute the python script:

```bash
$ python main.py
```

After running the application, you should see some text printed to the LCD screen - after
approximately 5 seconds, the screen will be cleared and the application will terminate.
