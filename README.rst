
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-CircuitPython_ADS1x15/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/CircuitPython_ADS1x15/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

Support for the ADS1x15 series of analog-to-digital converters. Available in 12-bit (ADS1015)
and 16-bit (ADS1115) versions.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Single Ended
------------

.. code-block:: python

  import board
  import busio
  from adafruit_ads1x15.single_ended import ADS1015

  i2c = busio.I2C(board.SCL, board.SDA)
  adc = ADS1015(i2c)
  while True:
      # channel 0
      print(adc[0].value, adc[0].volts)

Differential
------------

.. code-block:: python

  import board
  import busio
  from adafruit_ads1x15.differential import ADS1015

  i2c = busio.I2C(board.SCL, board.SDA)
  adc = ADS1015(i2c)
  while True:
      # channel 0 - channel 1
      print(adc[(0,1)].value, adc[(0,1)].volts)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPython_ADS1x15/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
