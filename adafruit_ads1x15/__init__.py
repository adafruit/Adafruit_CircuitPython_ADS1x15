# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
# SPDX-FileCopyrightText: 2025 Asadullah Shaikh <github.com/pantheraleo-7>
#
# SPDX-License-Identifier: MIT

"""
`adafruit_ads1x15`
====================================================

Support for the ADS1x15 series of analog-to-digital converters.

* Author(s): Carter Nelson
"""

from .ads1015 import ADS1015
from .ads1115 import ADS1115
from .analog_in import AnalogIn

__all__ = ["ADS1015", "ADS1115", "AnalogIn"]
