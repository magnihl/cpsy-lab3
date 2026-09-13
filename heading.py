"""Print the compass heading. Flat only.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python heading.py
Ctrl+C stops it.
"""

import math
import time

import adafruit_icm20x
import board
import busio

# hard iron offsets
OFF_X = 2.4
OFF_Y = 28.7
OFF_Z = 0.4

# rotate the zero onto the IMU edge
FRONT = 180

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)

while True:
    mx, my, mz = icm.magnetic
    mx = mx - OFF_X
    my = my - OFF_Y
    mz = mz - OFF_Z
    heading = (math.degrees(math.atan2(mx, my)) + FRONT) % 360

    print(f"heading {heading:6.1f}   mx {mx:6.1f}  my {my:6.1f}")
    time.sleep(0.5)
