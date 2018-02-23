import time
import board
import busio
from adafruit_ads1x15.differential import ADS1115

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
adc = ADS1115(i2c)

# Print header
print("CHAN 0 - CHAN 1")
print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    # Get raw reading for differential input between channel 0 and 1
    raw = adc[(0, 1)].value

    # Get voltage reading for differential input between channel 0 and 1
    volts = adc[(0, 1)].volts

    # Print results
    print("{:>5}\t{:>5.3f}".format(raw, volts))

    # Sleep for a bit
    time.sleep(0.5)
