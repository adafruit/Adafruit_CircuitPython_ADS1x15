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
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

repeats = 0

data = [None] * SAMPLES

start = time.monotonic()

# Read the same channel over and over
for i in range(SAMPLES):
    data[i] = chan0.value
    # Detect repeated values due to over polling
    if data[i] == data[i - 1]:
        repeats += 1


end = time.monotonic()
total_time = end - start

rate_reported = SAMPLES / total_time
rate_actual = (SAMPLES - repeats) / total_time
# NOTE: leave input floating to pickup some random noise
#       This cannot estimate conversion rates higher than polling rate

print("Took {:5.3f} s to acquire {:d} samples.".format(total_time, SAMPLES))
print("")
print("Configured:")
print("    Requested       = {:5d}    sps".format(RATE))
print("    Reported        = {:5d}    sps".format(ads.data_rate))
print("")
print("Actual:")
print("    Polling Rate    = {:8.2f} sps".format(rate_reported))
print("                      {:9.2%}".format(rate_reported / RATE))
print("    Repeats         = {:5d}".format(repeats))
print("    Conversion Rate = {:8.2f} sps   (estimated)".format(rate_actual))
