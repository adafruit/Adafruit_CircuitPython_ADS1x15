# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Create the I2C bus
i2c = board.I2C()

# Create the ADS object
# ads = ADS.ADS1015(i2c)
ads = ADS1115(i2c)

# Create a single-ended channel on Pin A0
#   Max counts for ADS1015 = 2047
#                  ADS1115 = 32767
chan = AnalogIn(ads, ads1x15.Pin.A0)

# The ADS1015 and ADS1115 both have the same gain options.
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256
#
gains = (2 / 3, 1, 2, 4, 8, 16)

while True:
    ads.gain = gains[0]
    print(f"{chan.value:5} {chan.voltage:5.3f}", end="")
    for gain in gains[1:]:
        ads.gain = gain
        print(f" | {chan.value:5} {chan.voltage:5.3f}", end="")
    print()
    time.sleep(0.5)
