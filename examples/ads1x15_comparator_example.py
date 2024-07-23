# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import countio

import adafruit_ads1x15.ads1015 as ADS
# import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS object
ads = ADS.ADS1015(i2c)
# ads = ADS.ADS1115(i2c)

# Create a single-ended channel on Pin 0
#   Max counts for ADS1015 = 2047
#                  ADS1115 = 32767
chan = AnalogIn(ads, ADS.P0)

# Create Interrupt-driven input to track comparator changes
int_pin = countio.Counter(board.GP9, edge=countio.Edge.RISE)

# Set comparator to assert after 1 ADC conversion
ads.compqueue = 1
# Set comparator low threshold to 2V
ads.write_comparator_low_threshold(chan.ADC_value(2))
# Set comparator high threshold to 2.002V. High threshold must be above low threshold
ads.write_comparator_high_threshold(chan.ADC_value(2.002))

count = 0
while True:
    print(chan.value, chan.voltage) #This initiates new ADC reading
    if int_pin.count > count:
        print("Comparator Triggered")
        count = int_pin.count
    time.sleep(2)
