# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`ads1115`
====================================================

CircuitPython driver for 1115 ADCs.

* Author(s): Carter Nelson
"""
import struct

# pylint: disable=unused-import
from .ads1x15 import ADS1x15, Mode

# Data sample rates
_ADS1115_CONFIG_DR = {
    8: 0x0000,
    16: 0x0020,
    32: 0x0040,
    64: 0x0060,
    128: 0x0080,
    250: 0x00A0,
    475: 0x00C0,
    860: 0x00E0,
}

# Pins
P0 = 0
P1 = 1
P2 = 2
P3 = 3


class ADS1115(ADS1x15):
    """Class for the ADS1115 16 bit ADC."""

    @property
    def bits(self):
        """The ADC bit resolution."""
        return 16

    @property
    def rates(self):
        """Possible data rate settings."""
        r = list(_ADS1115_CONFIG_DR.keys())
        r.sort()
        return r

    @property
    def rate_config(self):
        """Rate configuration masks."""
        return _ADS1115_CONFIG_DR

    def _data_rate_default(self) -> int:
        return 128

    def _conversion_value(self, raw_adc: int) -> int:
        raw_adc = raw_adc.to_bytes(2, "big")
        value = struct.unpack(">h", raw_adc)[0]
        return value
