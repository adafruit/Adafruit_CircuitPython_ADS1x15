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
`adafruit_ads1x15`
====================================================

CircuitPython driver for ADS1015/1115 ADCs.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15.git"

import time
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

# Register and other configuration values:
# pylint: disable=bad-whitespace
ADS1X15_DEFAULT_ADDRESS        = const(0x48)
ADS1X15_POINTER_CONVERSION     = const(0x00)
ADS1X15_POINTER_CONFIG         = const(0x01)
ADS1X15_POINTER_LOW_THRESHOLD  = const(0x02)
ADS1X15_POINTER_HIGH_THRESHOLD = const(0x03)
ADS1X15_CONFIG_OS_SINGLE       = const(0x8000)
ADS1X15_CONFIG_MUX_OFFSET      = const(12)
# Maping of gain values to config register values.
ADS1X15_CONFIG_GAIN = {
    2/3: 0x0000,
    1:   0x0200,
    2:   0x0400,
    4:   0x0600,
    8:   0x0800,
    16:  0x0A00
}
ADS1X15_PGA_RANGE = {
    2/3: 6.144,
    1:   4.096,
    2:   2.048,
    4:   1.024,
    8:   0.512,
    16:  0.256
}
ADS1X15_CONFIG_MODE_CONTINUOUS  = const(0x0000)
ADS1X15_CONFIG_MODE_SINGLE      = const(0x0100)
# Mapping of data/sample rate to config register values for ADS1015 (faster).
ADS1015_CONFIG_DR = {
    128:   0x0000,
    250:   0x0020,
    490:   0x0040,
    920:   0x0060,
    1600:  0x0080,
    2400:  0x00A0,
    3300:  0x00C0
}
# Mapping of data/sample rate to config register values for ADS1115 (slower).
ADS1115_CONFIG_DR = {
    8:    0x0000,
    16:   0x0020,
    32:   0x0040,
    64:   0x0060,
    128:  0x0080,
    250:  0x00A0,
    475:  0x00C0,
    860:  0x00E0
}
ADS1X15_CONFIG_COMP_WINDOW      = const(0x0010)
ADS1X15_CONFIG_COMP_ACTIVE_HIGH = const(0x0008)
ADS1X15_CONFIG_COMP_LATCHING    = const(0x0004)
ADS1X15_CONFIG_COMP_QUE = {
    1: 0x0000,
    2: 0x0001,
    4: 0x0002
}
ADS1X15_CONFIG_COMP_QUE_DISABLE = const(0x0003)
ADS1X15_DIFF_CHANNELS = {
    (0,1): 0,
    (0,3): 1,
    (1,3): 2,
    (2,3): 3
}
# pylint: enable=bad-whitespace

class ADC_Channel(object):
    """Provides per channel access to ADC readings."""

    def __init__(self, adc, channel):
        self._adc = adc
        self._channel = channel

    @property
    def value(self, ):
        """ADC reading in raw counts."""
        return self._adc._read_channel(self._channel) # pylint: disable=protected-access

    @property
    def volts(self, ):
        """ADC reading in volts."""
        return self._adc._read_channel_volts(self._channel) # pylint: disable=protected-access


class ADS1x15(object):
    """Base functionality for ADS1x15 analog to digital converters."""

    def __init__(self, i2c, address=ADS1X15_DEFAULT_ADDRESS):
        self.buf = bytearray(3)
        self.i2c_device = I2CDevice(i2c, address)
        self.bits = None
        self._channels = [ADC_Channel(self, 0),
                          ADC_Channel(self, 1),
                          ADC_Channel(self, 2),
                          ADC_Channel(self, 3)]

    def _write_register(self, reg, value):
        """Write 16 bit value to register."""
        self.buf[0] = reg
        self.buf[1] = (value >> 8) & 0xFF
        self.buf[2] = value & 0xFF
        with self.i2c_device as i2c:
            i2c.write(self.buf)

    def _read_register(self, reg):
        """Return 16 bit register value as tuple of (LSB, MSB)."""
        self.buf[0] = reg
        with self.i2c_device as i2c:
            i2c.write(self.buf, end=1, stop=False)
            i2c.readinto(self.buf, start=1)
        return self.buf[1] << 8 | self.buf[2]

    def _data_rate_default(self):
        """Retrieve the default data rate for this ADC (in samples per second).
        Should be implemented by subclasses.
        """
        raise NotImplementedError('Subclasses must implement _data_rate_default!')

    def _data_rate_config(self, data_rate):
        """Subclasses should override this function and return a 16-bit value
        that can be OR'ed with the config register to set the specified
        data rate.  If a value of None is specified then a default data_rate
        setting should be returned.  If an invalid or unsupported data_rate is
        provided then an exception should be thrown.
        """
        raise NotImplementedError('Subclass must implement _data_rate_config function!')

    def _conversion_value(self, low, high):
        """Subclasses should override this function that takes the low and high
        byte of a conversion result and returns a signed integer value.
        """
        raise NotImplementedError('Subclass must implement _conversion_value function!')

    def _read_channel(self, channel):
        """Subclasses should override this function to return a value for the
        requested channels as a signed integer value.
        """
        raise NotImplementedError('Subclass must implement _read_channel function!')

    def _read_channel_volts(self, channel):
        """Subclasses should override this function to return a value for the
        requested channels as a float value.
        """
        raise NotImplementedError('Subclass must implement _read_channel_volts function!')

    def _conversion_complete(self):
        """Return status of ADC conversion."""
        # OS is bit 15
        # OS = 0: Device is currently performing a conversion
        # OS = 1: Device is not currently performing a conversion
        return self._read_register(ADS1X15_POINTER_CONFIG) & 0x8000

    def _read(self, mux, gain, data_rate, mode):
        """Perform an ADC read with the provided mux, gain, data_rate, and mode
        values.  Returns the signed integer result of the read.
        """
        config = ADS1X15_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
        # Specify mux value.
        config |= (mux & 0x07) << ADS1X15_CONFIG_MUX_OFFSET
        # Validate the passed in gain and then set it in the config.
        if gain not in ADS1X15_CONFIG_GAIN:
            raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1X15_CONFIG_GAIN[gain]
        # Set the mode (continuous or single shot).
        config |= mode
        # Get the default data rate if none is specified (default differs between
        # ADS1015 and ADS1115).
        if data_rate is None:
            data_rate = self._data_rate_default()
        # Set the data rate (this is controlled by the subclass as it differs
        # between ADS1015 and ADS1115).
        config |= self._data_rate_config(data_rate)
        config |= ADS1X15_CONFIG_COMP_QUE_DISABLE  # Disble comparator mode.
        # Send the config value to start the ADC conversion.
        self._write_register(ADS1X15_POINTER_CONFIG, config)
        # Wait for conversion to complete
        while not self._conversion_complete():
            time.sleep(0.01)
        # Return the result
        return self.get_last_result()

    def stop_adc(self):
        """Stop all continuous ADC conversions (either normal or difference mode).
        """
        # Set the config register to its default value of 0x8583 to stop
        # continuous conversions.
        self._write_register(ADS1X15_POINTER_CONFIG, 0x8583)

    def get_last_result(self):
        """Read the last conversion result when in continuous conversion mode.
        Will return a signed integer value.
        """
        # Retrieve the conversion register value, convert to a signed int, and
        # return it.
        result = self._read_register(ADS1X15_POINTER_CONVERSION)
        return self._conversion_value(result & 0xff, result >> 8)
