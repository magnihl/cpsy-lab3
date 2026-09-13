"""Light the level LED when the board is flat.

Accelerometer only. Tilt is the angle between the board's vertical axis and
gravity: 0 flat, 90 on its side. Two thresholds so the LED does not flicker
when the tilt sits right on the boundary.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python level.py
"""

import math
import time

import adafruit_icm20x
import board
import busio
from gpiozero import LED

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)
led = LED(27)

ON_BELOW = 5.0     # degrees, LED turns on when tilt drops under this
OFF_ABOVE = 8.0    # degrees, LED turns off when tilt rises over this

while True:
    ax, ay, az = icm.acceleration
    total = math.sqrt(ax * ax + ay * ay + az * az)
    tilt = math.degrees(math.acos(az / total))

    if tilt < ON_BELOW:
        led.on()
    elif tilt > OFF_ABOVE:
        led.off()

    print(f"tilt {tilt:5.1f}   led {'ON ' if led.is_lit else 'off'}")
    time.sleep(0.2)
