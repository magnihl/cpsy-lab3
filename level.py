"""Light the level LED when the board is flat.

Accelerometer only. Tilt is the angle between the board's vertical axis and
gravity: 0 flat, 90 on its side. Two thresholds so the LED does not flicker
when the tilt sits right on the boundary.

Level means resting flat on the surface. Flat reads about 2.6 degrees on this
board because the sensor sits slightly crooked in its socket, so the on
threshold has to sit above that.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python level.py
"""

import math
import time

import adafruit_icm20x
import board
import busio
from gpiozero import LED

ON_BELOW = 4.0     # degrees, LED turns on when tilt drops under this
OFF_ABOVE = 6.0    # degrees, LED turns off when tilt rises over this

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)
led = LED(27)

while True:
    ax, ay, az = icm.acceleration
    total = math.sqrt(ax * ax + ay * ay + az * az)
    tilt = math.degrees(math.acos(az / total))

    if tilt < ON_BELOW:
        led.on()
    elif tilt > OFF_ABOVE:
        led.off()

    time.sleep(0.05)
