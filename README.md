# cpsy-lab3

Compass and level on a Raspberry Pi Zero with an ICM-20948 IMU.
Red LED lights when the board points north, second LED when it is level.

Runs on the Pi with the lab 2 environment, which already has the driver:

    ~/cpsy-display-ip/cpsy/bin/python raw.py
    ~/cpsy-display-ip/cpsy/bin/python collect.py

- `raw.py` prints unprocessed readings twice a second.
- `collect.py` records one averaged, labelled row per pose to `poses.csv`.

I2C address is 0x69, ADO tied high.
