# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`ads1x15`
====================================================

CircuitPython base class driver for ADS1015/1115 ADCs.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15.git"

import time

from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const

try:
    from typing import Dict, List, Optional

    from busio import I2C
    from microcontroller import Pin
except ImportError:
    # define Pin to avoid the error:
    #   def read(self, pin: Pin, is_differential: bool = False) -> int:
    #   NameError: name 'Pin' is not defined
    Pin = None

_ADS1X15_DEFAULT_ADDRESS = const(0x48)
_ADS1X15_POINTER_CONVERSION = const(0x00)
_ADS1X15_POINTER_CONFIG = const(0x01)
_ADS1X15_POINTER_LO_THRES = const(0x02)
_ADS1X15_POINTER_HI_THRES = const(0x03)

_ADS1X15_CONFIG_OS_SINGLE = const(0x8000)
_ADS1X15_CONFIG_MUX_OFFSET = const(12)
_ADS1X15_CONFIG_COMP_QUEUE = {
    0: 0x0003,
    1: 0x0000,
    2: 0x0001,
    4: 0x0002,
}
_ADS1X15_CONFIG_GAIN = {
    2 / 3: 0x0000,
    1: 0x0200,
    2: 0x0400,
    4: 0x0600,
    8: 0x0800,
    16: 0x0A00,
}


class Mode:
    """An enum-like class representing possible ADC operating modes."""

    # See datasheet "Operating Modes" section
    # values here are masks for setting MODE bit in Config Register
    # pylint: disable=too-few-public-methods
    CONTINUOUS = 0x0000
    """Continuous Mode"""
    SINGLE = 0x0100
    """Single-Shot Mode"""


class ADS1x15:
    """Base functionality for ADS1x15 analog to digital converters.

    :param ~busio.I2C i2c: The I2C bus the device is connected to.
    :param float gain: The ADC gain.
    :param int data_rate: The data rate for ADC conversion in samples per second.
                          Default value depends on the device.
    :param Mode mode: The conversion mode, defaults to `Mode.SINGLE`.
    :param int comparator_queue_length: The number of successive conversions exceeding
                          the comparator threshold before asserting ALERT/RDY pin.
                          Defaults to 0 (comparator function disabled).
    :param int comparator_low_threshold: Voltage limit under which comparator de-asserts
                          ALERT/RDY pin. Must be lower than high threshold to use comparator
                          function. See subclass for value range and default.
    :param int comparator_high_threshold: Voltage limit over which comparator asserts
                          ALERT/RDY pin. Must be higher than low threshold to use comparator
                          function. See subclass for value range and default.
    :param int address: The I2C address of the device.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        i2c: I2C,
        gain: float = 1,
        data_rate: Optional[int] = None,
        mode: int = Mode.SINGLE,
        comparator_queue_length: int = 0,
        comparator_low_threshold: int = -32768,
        comparator_high_threshold: int = 32767,
        address: int = _ADS1X15_DEFAULT_ADDRESS,
    ):
        # pylint: disable=too-many-arguments
        self._last_pin_read = None
        self.buf = bytearray(3)
        self.gain = gain
        self.data_rate = self._data_rate_default() if data_rate is None else data_rate
        self.mode = mode
        self.comparator_queue_length = comparator_queue_length
        self.i2c_device = I2CDevice(i2c, address)
        self.comparator_low_threshold = comparator_low_threshold
        self.comparator_high_threshold = comparator_high_threshold

    @property
    def bits(self) -> int:
        """The ADC bit resolution."""
        raise NotImplementedError("Subclass must implement bits property.")

    @property
    def data_rate(self) -> int:
        """The data rate for ADC conversion in samples per second."""
        return self._data_rate

    @data_rate.setter
    def data_rate(self, rate: int) -> None:
        possible_rates = self.rates
        if rate not in possible_rates:
            raise ValueError("Data rate must be one of: {}".format(possible_rates))
        self._data_rate = rate

    @property
    def rates(self) -> List[int]:
        """Possible data rate settings."""
        raise NotImplementedError("Subclass must implement rates property.")

    @property
    def rate_config(self) -> Dict[int, int]:
        """Rate configuration masks."""
        raise NotImplementedError("Subclass must implement rate_config property.")

    @property
    def gain(self) -> float:
        """The ADC gain."""
        return self._gain

    @gain.setter
    def gain(self, gain: float) -> None:
        possible_gains = self.gains
        if gain not in possible_gains:
            raise ValueError("Gain must be one of: {}".format(possible_gains))
        self._gain = gain

    @property
    def gains(self) -> List[float]:
        """Possible gain settings."""
        g = list(_ADS1X15_CONFIG_GAIN.keys())
        g.sort()
        return g

    @property
    def comparator_queue_length(self) -> int:
        """The ADC comparator queue length."""
        return self._comparator_queue_length

    @comparator_queue_length.setter
    def comparator_queue_length(self, comparator_queue_length: int) -> None:
        possible_comp_queue_lengths = self.comparator_queue_lengths
        if comparator_queue_length not in possible_comp_queue_lengths:
            raise ValueError(
                "Comparator Queue must be one of: {}".format(
                    possible_comp_queue_lengths
                )
            )
        self._comparator_queue_length = comparator_queue_length

    @property
    def comparator_queue_lengths(self) -> List[int]:
        """Possible comparator queue length settings."""
        g = list(_ADS1X15_CONFIG_COMP_QUEUE.keys())
        g.sort()
        return g

    @property
    def comparator_low_threshold(self) -> int:
        """The ADC Comparator Lower Limit Threshold."""
        return self._comparator_low_threshold

    @property
    def comparator_high_threshold(self) -> int:
        """The ADC Comparator Higher Limit Threshold."""
        return self._comparator_high_threshold

    @comparator_low_threshold.setter
    def comparator_low_threshold(self, value: int) -> None:
        """Set comparator low threshold value for ADS1x15 ADC

        :param int value: 16-bit signed integer to write to register
        """
        if value < -32768 or value > 32767:
            raise ValueError(
                "Comparator Threshold value must be between -32768 and 32767"
            )

        self._comparator_low_threshold = value
        self._write_register(_ADS1X15_POINTER_LO_THRES, self.comparator_low_threshold)

    @comparator_high_threshold.setter
    def comparator_high_threshold(self, value: int) -> None:
        """Set comparator high threshold value for ADS1x15 ADC

        :param int value: 16-bit signed integer to write to register
        """
        if value < -32768 or value > 32767:
            raise ValueError(
                "Comparator Threshold value must be between -32768 and 32767"
            )

        self._comparator_high_threshold = value
        self._write_register(_ADS1X15_POINTER_HI_THRES, self.comparator_high_threshold)

    @property
    def mode(self) -> int:
        """The ADC conversion mode."""
        return self._mode

    @mode.setter
    def mode(self, mode: int) -> None:
        if mode not in (Mode.CONTINUOUS, Mode.SINGLE):
            raise ValueError("Unsupported mode.")
        self._mode = mode

    def read(self, pin: Pin, is_differential: bool = False) -> int:
        """I2C Interface for ADS1x15-based ADCs reads.

        :param ~microcontroller.Pin pin: individual or differential pin.
        :param bool is_differential: single-ended or differential read.
        """
        pin = pin if is_differential else pin + 0x04
        return self._read(pin)

    def _data_rate_default(self) -> int:
        """Retrieve the default data rate for this ADC (in samples per second).
        Should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _data_rate_default!")

    def _conversion_value(self, raw_adc: int) -> int:
        """Subclasses should override this function that takes the 16 raw ADC
        values of a conversion result and returns a signed integer value.
        """
        raise NotImplementedError("Subclass must implement _conversion_value function!")

    def _read(self, pin: Pin) -> int:
        """Perform an ADC read. Returns the signed integer result of the read."""
        # Immediately return conversion register result if in CONTINUOUS mode
        # and pin has not changed
        if self.mode == Mode.CONTINUOUS and self._last_pin_read == pin:
            return self._conversion_value(self.get_last_result(True))

        # Assign last pin read if in SINGLE mode or first sample in CONTINUOUS mode on this pin
        self._last_pin_read = pin

        # Configure ADC every time before a conversion in SINGLE mode
        # or changing channels in CONTINUOUS mode
        if self.mode == Mode.SINGLE:
            config = _ADS1X15_CONFIG_OS_SINGLE
        else:
            config = 0
        config |= (pin & 0x07) << _ADS1X15_CONFIG_MUX_OFFSET
        config |= _ADS1X15_CONFIG_GAIN[self.gain]
        config |= self.mode
        config |= self.rate_config[self.data_rate]
        config |= _ADS1X15_CONFIG_COMP_QUEUE[self.comparator_queue_length]
        self._write_register(_ADS1X15_POINTER_CONFIG, config)

        # Wait for conversion to complete
        # ADS1x1x devices settle within a single conversion cycle
        if self.mode == Mode.SINGLE:
            # Continuously poll conversion complete status bit
            while not self._conversion_complete():
                pass
        else:
            # Can't poll registers in CONTINUOUS mode
            # Wait expected time for two conversions to complete
            time.sleep(2 / self.data_rate)

        return self._conversion_value(self.get_last_result(False))

    def _conversion_complete(self) -> int:
        """Return status of ADC conversion."""
        # OS is bit 15
        # OS = 0: Device is currently performing a conversion
        # OS = 1: Device is not currently performing a conversion
        return self._read_register(_ADS1X15_POINTER_CONFIG) & 0x8000

    def get_last_result(self, fast: bool = False) -> int:
        """Read the last conversion result when in continuous conversion mode.
        Will return a signed integer value. If fast is True, the register
        pointer is not updated as part of the read. This reduces I2C traffic
        and increases possible read rate.
        """
        return self._read_register(_ADS1X15_POINTER_CONVERSION, fast)

    def _write_register(self, reg: int, value: int):
        """Write 16 bit value to register."""
        self.buf[0] = reg
        self.buf[1] = (value >> 8) & 0xFF
        self.buf[2] = value & 0xFF
        with self.i2c_device as i2c:
            i2c.write(self.buf)

    def _read_register(self, reg: int, fast: bool = False) -> int:
        """Read 16 bit register value. If fast is True, the pointer register
        is not updated.
        """
        with self.i2c_device as i2c:
            if fast:
                i2c.readinto(self.buf, end=2)
            else:
                i2c.write_then_readinto(bytearray([reg]), self.buf, in_end=2)
        return self.buf[0] << 8 | self.buf[1]
