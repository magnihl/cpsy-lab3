"""Print raw IMU readings, no calculation.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python raw.py
Ctrl+C stops it.
"""

import time

import adafruit_icm20x
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)

while True:
    ax, ay, az = icm.acceleration
    mx, my, mz = icm.magnetic
    print(f"accel {ax:7.2f} {ay:7.2f} {az:7.2f}   mag {mx:7.1f} {my:7.1f} {mz:7.1f}")
    time.sleep(0.5)
