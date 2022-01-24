Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ads1x15/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ads1x15/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/actions/
    :alt: Build Status

Support for the ADS1x15 series of analog-to-digital converters. Available in 12-bit (ADS1015)
and 16-bit (ADS1115) versions.

Installation & Dependencies
===========================

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This can be most easily achieved by downloading and installing
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_ on
your device.

Installing from PyPI
--------------------

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ads1x15/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ads1x15

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ads1x15

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ads1x15

Usage Example
=============

Single Ended
------------

.. code-block:: python

    import time
    import board
    import busio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1015(i2c)

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)

    # Create differential input between channel 0 and 1
    #chan = AnalogIn(ads, ADS.P0, ADS.P1)

    print("{:>5}\t{:>5}".format('raw', 'v'))

    while True:
        print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
        time.sleep(0.5)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ads1x15/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPython_ADS1x15/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
