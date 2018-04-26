
Build Status

[![Build Status](https://travis-ci.org/lihan/dj-currencies.svg?branch=master)](https://travis-ci.org/lihan/dj-currencies)

Documentation
-------------

The full documentation is at https://dj-currencies.readthedocs.io.

Quickstart
----------

Install djcurrencies::

    pip install dj-currencies

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_currencies.apps.DjCurrenciesConfig',
        ...
    )


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

