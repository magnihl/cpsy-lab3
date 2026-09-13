"""Blink one LED, no sensor. Proves the LED wiring and the pin number.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python blink.py
Ctrl+C stops it.
"""

from time import sleep

from gpiozero import LED

led = LED(27)
while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
