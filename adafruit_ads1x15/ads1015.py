# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`ads1015`
====================================================

CircuitPython driver for ADS1015 ADCs.

* Author(s): Carter Nelson
"""
import struct

# pylint: disable=unused-import
from .ads1x15 import ADS1x15, Mode

# Data sample rates
_ADS1015_CONFIG_DR = {
    128: 0x0000,
    250: 0x0020,
    490: 0x0040,
    920: 0x0060,
    1600: 0x0080,
    2400: 0x00A0,
    3300: 0x00C0,
}

# Pins
P0 = 0
P1 = 1
P2 = 2
P3 = 3


class ADS1015(ADS1x15):
    """Class for the ADS1015 12 bit ADC."""

    @property
    def bits(self):
        """The ADC bit resolution."""
        return 12

    @property
    def rates(self):
        """Possible data rate settings."""
        r = list(_ADS1015_CONFIG_DR.keys())
        r.sort()
        return r

    @property
    def rate_config(self):
        """Rate configuration masks."""
        return _ADS1015_CONFIG_DR

    def _data_rate_default(self) -> int:
        return 1600

    def _conversion_value(self, raw_adc: int) -> int:
        raw_adc = raw_adc.to_bytes(2, "big")
        value = struct.unpack(">h", raw_adc)[0]
        return value >> 4
