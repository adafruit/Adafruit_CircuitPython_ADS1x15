import time
import board
import busio
from adafruit_ads1x15.single_ended import ADS1115

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
adc = ADS1115(i2c)

# Print header
print("    CHAN 0          CHAN 1          CHAN 2          CHAN 3")
print("{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}"
      .format('raw', 'v', 'raw', 'v', 'raw', 'v', 'raw', 'v'))

while True:
    # Get raw readings for each channel
    r0 = adc[0].value
    r1 = adc[1].value
    r2 = adc[2].value
    r3 = adc[3].value

    # Get voltage readings for each channel
    v0 = adc[0].volts
    v1 = adc[1].volts
    v2 = adc[2].volts
    v3 = adc[3].volts

    # Print results
    print("{:>5}\t{:>5.3f}\t{:>5}\t{:>5.3f}\t{:>5}\t{:>5.3f}\t{:>5}\t{:>5.3f}"
          .format(r0, v0, r1, v1, r2, v2, r3, v3))

    # Sleep for a bit
    time.sleep(0.5)
