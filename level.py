"""Light the level LED when the board is flat.

Accelerometer only. Tilt is the angle between the board's vertical axis and
gravity: 0 flat, 90 on its side. Two thresholds so the LED does not flicker
when the tilt sits right on the boundary.

Prints a line only when the LED changes state, and appends the same line to
level_log.csv, so the terminal stays quiet while you tilt.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python level.py
"""

import csv
import math
import os
import time

import adafruit_icm20x
import board
import busio
from gpiozero import LED

ON_BELOW = 5.0     # degrees, LED turns on when tilt drops under this
OFF_ABOVE = 8.0    # degrees, LED turns off when tilt rises over this
FILE = "level_log.csv"

i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x69)
led = LED(27)


def tilt_degrees():
    ax, ay, az = icm.acceleration
    total = math.sqrt(ax * ax + ay * ay + az * az)
    return math.degrees(math.acos(az / total))


new = not os.path.exists(FILE)
with open(FILE, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["time", "state", "tilt_deg"])

    was_lit = led.is_lit
    print(f"on below {ON_BELOW}, off above {OFF_ABOVE}. Tilt away, Ctrl+C to stop.")

    while True:
        tilt = tilt_degrees()

        if tilt < ON_BELOW:
            led.on()
        elif tilt > OFF_ABOVE:
            led.off()

        if led.is_lit != was_lit:
            state = "ON" if led.is_lit else "OFF"
            print(f"{state:<3} at tilt {tilt:5.1f}")
            w.writerow([time.strftime("%H:%M:%S"), state, round(tilt, 1)])
            f.flush()
            was_lit = led.is_lit

        time.sleep(0.05)
