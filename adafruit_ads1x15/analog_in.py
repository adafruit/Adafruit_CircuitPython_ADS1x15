# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`analog_in`
==============================
AnalogIn for single-ended and
differential ADC readings.

* Author(s): Carter Nelson, adapted from MCP3xxx original by Brent Rubell
"""

try:
    from typing import Optional

    from .ads1x15 import ADS1x15
except ImportError:
    pass

_ADS1X15_DIFF_CHANNELS = {(0, 1): 0, (0, 3): 1, (1, 3): 2, (2, 3): 3}
_ADS1X15_PGA_RANGE = {2 / 3: 6.144, 1: 4.096, 2: 2.048, 4: 1.024, 8: 0.512, 16: 0.256}


class AnalogIn:
    """AnalogIn Mock Implementation for ADC Reads.

    :param ADS1x15 ads: The ads object.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.
    """

    def __init__(self, ads: ADS1x15, positive_pin: int, negative_pin: Optional[int] = None):
        self._ads = ads
        self._pin_setting = positive_pin
        self._negative_pin = negative_pin
        self.is_differential = False
        if negative_pin is not None:
            pins = (self._pin_setting, self._negative_pin)
            if pins not in _ADS1X15_DIFF_CHANNELS:
                raise ValueError(
                    f"Differential channels must be one of: {list(_ADS1X15_DIFF_CHANNELS.keys())}"
                )
            self._pin_setting = _ADS1X15_DIFF_CHANNELS[pins]
            self.is_differential = True

    @property
    def value(self) -> int:
        """The value on the analog pin between 0 and 65535
        inclusive (16-bit). (read-only)

        Even if the underlying analog to digital converter (ADC) is
        lower resolution, the value is 16-bit.
        """
        pin = self._pin_setting if self.is_differential else self._pin_setting + 0x04
        return self._ads.read(pin)

    @property
    def voltage(self) -> float:
        """Returns the voltage from the ADC pin as a floating point value."""
        volts = self.convert_to_voltage(self.value)
        return volts

    def convert_to_value(self, volts: float) -> int:
        """Calculates a standard 16-bit integer value for a given voltage"""

        lsb = _ADS1X15_PGA_RANGE[self._ads.gain] / (1 << (self._ads.bits - 1))
        value = int(volts / lsb)

        # Need to bit shift if value is only 12-bits
        value <<= 16 - self._ads.bits
        return value

    def convert_to_voltage(self, value_int: int) -> float:
        """Calculates voltage from 16-bit ADC reading"""

        lsb = _ADS1X15_PGA_RANGE[self._ads.gain] / (1 << (self._ads.bits - 1))

        # Need to bit shift if value is only 12-bits
        value_int >>= 16 - self._ads.bits
        volts = value_int * lsb

        return volts
