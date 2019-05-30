import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

# Data collection setup
RATE = 3300
SAMPLES = 1000

# Create the I2C bus
# Set frequency high to reduce time spent with I2C comms
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

# Create list to store data samples
data = [None]*SAMPLES

start = time.monotonic()

# Use a context manager to utilize fast reading of a channel
with chan0 as chan:
    # no other channels can be accessed inside here
    for i in range(SAMPLES):
        data[i] = chan.value
        # some form of conversion complete synchronization
        # should go here, but currently there is no efficient
        # way to do this

end = time.monotonic()
total_time = end - start

print("Time of capture: {}s".format(total_time))
print("Sample rate requested={} actual={}".format(RATE, SAMPLES / total_time))
