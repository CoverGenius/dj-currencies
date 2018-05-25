

.. image:: https://travis-ci.org/brightwrite/dj-currencies.svg?branch=master
    :target: https://travis-ci.org/brightwrite/dj-currencies

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
        'dj_currencies',
        ...
    )

Settings
========

.. code-blocks:: python

    DJANGO_CURRENCIES = {
        'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
        'OPENEXCHANGE_APP_ID': '',
        'BASE_CURRENCIES': 'USD',
        'MAX_CACHE_DAYS': 7
    }

You will need to have at least "OPENEXCHANGE_APP_ID" configured

*s*fsd

Features
--------

* [open exchange rates](openexchangerates.org) integration
* Extensible backend design, hook your own exchange rate sources
* Store historical exchange rates
* offline currency conversion

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ python runtests.py
