from .adafruit_ads1x15 import *

class ADS1x15_SingleEnded(ADS1x15):
    """Base functionality for ADS1x15 analog to digital converters operating
    in single ended mode."""

    def __getitem__(self, key):
        return self._channels[key]

    def read_adc(self, channel, gain=1, data_rate=None):
        """Read a single ADC channel and return the ADC value as a signed integer
        result.  Channel must be a value within 0-3.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Perform a single shot read and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        return self._read(channel + 0x04, gain, data_rate, ADS1x15_CONFIG_MODE_SINGLE)

    def read_volts(self, channel, gain=1, data_rate=None):
        """Read a single ADC channel and return the voltage value as a floating point
        result.  Channel must be a value within 0-3.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        raw = self.read_adc(channel, gain, data_rate)
        volts = raw * (ADS1x15_PGA_RANGE[gain] / (2**(self.bits-1) - 1))
        return volts

    def start_adc(self, channel, gain=1, data_rate=None):
        """Start continuous ADC conversions on the specified channel (0-3). Will
        return an initial conversion result, then call the get_last_result()
        function to read the most recent conversion result. Call stop_adc() to
        stop conversions.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Start continuous reads and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        return self._read(channel + 0x04, gain, data_rate, ADS1x15_CONFIG_MODE_CONTINUOUS)

class ADS1015(ADS1x15_SingleEnded):
    """ADS1015 12-bit single ended analog to digital converter instance."""

    def __init__(self, *args, **kwargs):
        super(ADS1015, self).__init__(*args, **kwargs)
        self.bits = 12

    def _data_rate_default(self):
        # Default from datasheet page 19, config register DR bit default.
        return 1600

    def _data_rate_config(self, data_rate):
        if data_rate not in ADS1015_CONFIG_DR:
            raise ValueError('Data rate must be one of: 128, 250, 490, 920, 1600, 2400, 3300')
        return ADS1015_CONFIG_DR[data_rate]

    def _conversion_value(self, low, high):
        # Convert to 12-bit signed value.
        value = ((high & 0xFF) << 4) | ((low & 0xFF) >> 4)
        # Check for sign bit and turn into a negative value if set.
        if value & 0x800 != 0:
            value -= 1 << 12
        return value

    def _read_channel(self, channel):
        return self.read_adc(channel)

    def _read_channel_volts(self, channel):
        return self.read_volts(channel)


class ADS1115(ADS1x15_SingleEnded):
    """ADS1115 16-bit single ended analog to digital converter instance."""

    def __init__(self, *args, **kwargs):
        super(ADS1115, self).__init__(*args, **kwargs)
        self.bits = 16

    def _data_rate_default(self):
        # Default from datasheet page 16, config register DR bit default.
        return 128

    def _data_rate_config(self, data_rate):
        if data_rate not in ADS1115_CONFIG_DR:
            raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
        return ADS1115_CONFIG_DR[data_rate]

    def _conversion_value(self, low, high):
        # Convert to 16-bit signed value.
        value = ((high & 0xFF) << 8) | (low & 0xFF)
        # Check for sign bit and turn into a negative value if set.
        if value & 0x8000 != 0:
            value -= 1 << 16
        return value

    def _read_channel(self, channel):
        return self.read_adc(channel)

    def _read_channel_volts(self, channel):
        return self.read_volts(channel)
