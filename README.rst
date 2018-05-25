

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


.. code-block:: python

    DJANGO_CURRENCIES = {
        'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
        'OPENEXCHANGE_APP_ID': '',
        'BASE_CURRENCIES': ['USD'],
        'MAX_CACHE_DAYS': 7
    }

**DEFAULT_BACKEND**: The selected backend to sync exchange rates

**OPENEXCHANGE_APP_ID**: Must be configured if you use **OpenExchangeBackend**

**BASE_CURRENCIES**: A list of base currencies to use. At the time of this version, you will only be able to convert currency from any one of the base currency to target currency.

**MAX_CACHE_DAYS**: Only use the cache within this time limit. If exchange rates was not synced within the time frame, an exception will thrown

.. NOTE::
   You will need to have at least "OPENEXCHANGE_APP_ID" configured if you use **OpenExchangeBackend**



Features
--------

* [open exchange rates](openexchangerates.org) integration
* Extensible backend design, hook your own exchange rate sources
* Multi base currencies support, no double conversion to lose precision
* Store historical exchange rates
* offline currency conversion

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ python runtests.py
