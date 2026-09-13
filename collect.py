"""Record one averaged reading per pose, labelled, to poses.csv.

Hold the board in a pose, type a name for it, press enter. Averages N
samples over about a second and appends one row. Blank name quits.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python collect.py
"""

import csv
import os
import time

import adafruit_icm20x
import board
import busio

N = 20
FILE = "poses.csv"

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)


def average():
    sums = [0.0] * 6
    for _ in range(N):
        a = icm.acceleration
        m = icm.magnetic
        for i in range(3):
            sums[i] += a[i]
            sums[i + 3] += m[i]
        time.sleep(0.05)
    return [s / N for s in sums]


new = not os.path.exists(FILE)
with open(FILE, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["label", "ax", "ay", "az", "mx", "my", "mz"])
    while True:
        label = input("pose (blank to quit): ").strip()
        if not label:
            break
        v = average()
        w.writerow([label] + [round(x, 2) for x in v])
        f.flush()
        print(f"  accel {v[0]:6.2f} {v[1]:6.2f} {v[2]:6.2f}   mag {v[3]:6.1f} {v[4]:6.1f} {v[5]:6.1f}")
