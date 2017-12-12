# The MIT License (MIT)
#
# Copyright (c) 2017 Carter Nelson for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ads1x15.single_ended`
====================================================

Single-ended driver for ADS1015/1115 ADCs.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15.git"

from .adafruit_ads1x15 import ADS1x15
from .adafruit_ads1x15 import ADS1X15_CONFIG_MODE_SINGLE, ADS1X15_CONFIG_MODE_CONTINUOUS
from .adafruit_ads1x15 import ADS1X15_PGA_RANGE, ADS1015_CONFIG_DR, ADS1115_CONFIG_DR

# pylint: disable=abstract-method
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
        return self._read(channel + 0x04, gain, data_rate, ADS1X15_CONFIG_MODE_SINGLE)

    def read_volts(self, channel, gain=1, data_rate=None):
        """Read a single ADC channel and return the voltage value as a floating point
        result.  Channel must be a value within 0-3.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        raw = self.read_adc(channel, gain, data_rate)
        volts = raw * (ADS1X15_PGA_RANGE[gain] / (2**(self.bits-1) - 1))
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
        return self._read(channel + 0x04, gain, data_rate, ADS1X15_CONFIG_MODE_CONTINUOUS)
# pylint: enable=abstract-method

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
