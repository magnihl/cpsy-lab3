"""Drive both LEDs from one sensor read per loop. Green when the board is
level, red when the IMU edge points at magnetic north.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python compass.py
Ctrl+C stops it.
"""

import math
import time

import adafruit_icm20x
import board
import busio
from gpiozero import LED

# level, degrees of tilt
LEVEL_ON = 4.0
LEVEL_OFF = 8.0

# north, degrees away from 0
NORTH_ON = 10.0
NORTH_OFF = 15.0

# hard iron offsets, uT
OFF_X = 2.4
OFF_Y = 28.7

# rotate the zero onto the IMU edge
FRONT = 0

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)
green = LED(27)
red = LED(22)

while True:
    ax, ay, az = icm.acceleration
    mx, my, mz = icm.magnetic

    total = math.sqrt(ax * ax + ay * ay + az * az)
    tilt = math.degrees(math.acos(az / total))

    mx = mx - OFF_X
    my = my - OFF_Y
    heading = (math.degrees(math.atan2(mx, my)) + FRONT) % 360
    off_north = min(heading, 360 - heading)

    if tilt < LEVEL_ON:
        green.on()
    elif tilt > LEVEL_OFF:
        green.off()

    if off_north < NORTH_ON:
        red.on()
    elif off_north > NORTH_OFF:
        red.off()

    time.sleep(0.05)
