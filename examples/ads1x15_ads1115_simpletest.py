# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Create the I2C bus
i2c = board.I2C()

# Create the ADC object using the I2C bus
ads = ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ads1x15.Pin.A0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ads1x15.Pin.A0, ads1x15.Pin.A1)

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print(f"{chan.value:>5}\t{chan.voltage:>5.3f}")
    time.sleep(0.5)
