# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import busio
import countio

import adafruit_ads1x15.ads1015 as ADS

# import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Comp_Latch, Comp_Mode, Comp_Polarity, Mode
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

# Set ADC to continuously read new data
ads.mode = Mode.CONTINUOUS
# Set comparator to assert after 1 ADC conversion
ads.comparator_queue_length = 1
# Set comparator to use traditional threshold instead of window
ads.comparator_mode = Comp_Mode.TRADITIONAL
# Set comparator output to de-assert if readings no longer above threshold
ads.comparator_latch = Comp_Latch.NONLATCHING
# Set comparator output to logic LOW when asserted
ads.comparator_polarity = Comp_Polarity.ACTIVE_LOW
# Gain should be explicitly set to ensure threshold values are calculated correctly
ads.gain = 1
# Set comparator low threshold to 2V
ads.comparator_low_threshold = chan.convert_to_value(2.000)
# Set comparator high threshold to 2.002V. High threshold must be above low threshold
ads.comparator_high_threshold = chan.convert_to_value(2.002)

count = 0
while True:
    print(chan.value, chan.voltage)  # This initiates new ADC reading
    if int_pin.count > count:
        print("Comparator Triggered")
        count = int_pin.count
    time.sleep(2)
