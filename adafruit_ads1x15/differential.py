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
`adafruit_ads1x15.differential`
====================================================

Differential driver for ADS1015/1115 ADCs.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15.git"

from .adafruit_ads1x15 import ADS1x15, ADS1X15_DIFF_CHANNELS
from .adafruit_ads1x15 import ADS1X15_CONFIG_MODE_SINGLE, ADS1X15_CONFIG_MODE_CONTINUOUS
from .adafruit_ads1x15 import ADS1X15_PGA_RANGE, ADS1015_CONFIG_DR, ADS1115_CONFIG_DR

# pylint: disable=abstract-method
class ADS1x15_Differential(ADS1x15):
    """Base functionality for ADS1x15 analog to digital converters operating
    in differential mode."""

    def __getitem__(self, key):
        return self._channels[ADS1X15_DIFF_CHANNELS[key]]

    def read_adc_difference(self, differential, gain=1, data_rate=None):
        """Read the difference between two ADC channels and return the ADC value
        as a signed integer result.  Differential must be one of:
        - 0 = Channel 0 minus channel 1
        - 1 = Channel 0 minus channel 3
        - 2 = Channel 1 minus channel 3
        - 3 = Channel 2 minus channel 3
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        # Perform a single shot read using the provided differential value
        # as the mux value (which will enable differential mode).
        return self._read(differential, gain, data_rate, ADS1X15_CONFIG_MODE_SINGLE)

    def read_volts_difference(self, differential, gain=1, data_rate=None):
        """Read the difference between two ADC channels and return the voltage value
        as a floating point result.  Differential must be one of:
        - 0 = Channel 0 minus channel 1
        - 1 = Channel 0 minus channel 3
        - 2 = Channel 1 minus channel 3
        - 3 = Channel 2 minus channel 3
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        raw = self.read_adc_difference(differential, gain, data_rate)
        volts = raw * (ADS1X15_PGA_RANGE[gain] / (2**(self.bits-1) - 1))
        return volts

    def start_adc_difference(self, differential, gain=1, data_rate=None):
        """Start continuous ADC conversions between two ADC channels. Differential
        must be one of:
        - 0 = Channel 0 minus channel 1
        - 1 = Channel 0 minus channel 3
        - 2 = Channel 1 minus channel 3
        - 3 = Channel 2 minus channel 3
        Will return an initial conversion result, then call the get_last_result()
        function continuously to read the most recent conversion result.  Call
        stop_adc() to stop conversions.
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        # Perform a single shot read using the provided differential value
        # as the mux value (which will enable differential mode).
        return self._read(differential, gain, data_rate, ADS1X15_CONFIG_MODE_CONTINUOUS)
# pylint: enable=abstract-method

class ADS1015(ADS1x15_Differential):
    """ADS1015 12-bit differential analog to digital converter instance."""

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
        return self.read_adc_difference(channel)

    def _read_channel_volts(self, channel):
        return self.read_volts_difference(channel)


class ADS1115(ADS1x15_Differential):
    """ADS1115 16-bit differential analog to digital converter instance."""

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
        return self.read_adc_difference(channel)

    def _read_channel_volts(self, channel):
        return self.read_volts_difference(channel)
