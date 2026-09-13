"""Blink both LEDs in turn, no sensor. Proves the LED wiring and the pin
numbers. Green first, then red, half a second each.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python blink.py
Ctrl+C stops it.
"""

from time import sleep

from gpiozero import LED

green = LED(27)   # level LED, physical pin 13
red = LED(22)     # north LED, physical pin 15

while True:
    green.on()
    red.off()
    sleep(0.5)
    green.off()
    red.on()
    sleep(0.5)
