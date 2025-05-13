# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import busio

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

# Data collection setup
RATE = 3300
SAMPLES = 1000

# Create the I2C bus with a fast frequency
# NOTE: Your device may not respect the frequency setting
#       Raspberry Pis must change this in /boot/config.txt

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

# First ADC channel read in continuous mode configures device
# and waits 2 conversion cycles
_ = chan0.value

sample_interval = 1.0 / ads.data_rate

repeats = 0
skips = 0

data = [None] * SAMPLES

start = time.monotonic()
time_next_sample = start + sample_interval

# Read the same channel over and over
for i in range(SAMPLES):
    # Wait for expected conversion finish time
    while time.monotonic() < (time_next_sample):
        pass

    # Read conversion value for ADC channel
    data[i] = chan0.value

    # Loop timing
    time_last_sample = time.monotonic()
    time_next_sample = time_next_sample + sample_interval
    if time_last_sample > (time_next_sample + sample_interval):
        skips += 1
        time_next_sample = time.monotonic() + sample_interval

    # Detect repeated values due to over polling
    if data[i] == data[i - 1]:
        repeats += 1

end = time.monotonic()
total_time = end - start

rate_reported = SAMPLES / total_time
rate_actual = (SAMPLES - repeats) / total_time
# NOTE: leave input floating to pickup some random noise
#       This cannot estimate conversion rates higher than polling rate

print(f"Took {total_time:5.3f} s to acquire {SAMPLES:d} samples.")
print("")
print("Configured:")
print(f"    Requested       = {RATE:5d}    sps")
print(f"    Reported        = {ads.data_rate:5d}    sps")
print("")
print("Actual:")
print(f"    Polling Rate    = {rate_reported:8.2f} sps")
print(f"                      {rate_reported / RATE:9.2%}")
print(f"    Skipped         = {skips:5d}")
print(f"    Repeats         = {repeats:5d}")
print(f"    Conversion Rate = {rate_actual:8.2f} sps   (estimated)")
