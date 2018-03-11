
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-CircuitPython_ADS1x15/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/CircuitPython_ADS1x15/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/Adafruit_CircuitPython_ADS1x15.svg?branch=master
    :target: https://travis-ci.org/adafruit/Adafruit_CircuitPython_ADS1x15
    :alt: Build Status

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

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-ads1x15 --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.

