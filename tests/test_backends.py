from __future__ import unicode_literals
from decimal import Decimal
from unittest import TestCase
from django.core.exceptions import ImproperlyConfigured
from dj_currencies.apis import convert_money
from dj_currencies.backends import OpenExchangeBackend
from dj_currencies.factory import ExchangeRateFactory
from dj_currencies.settings import currency_settings


class OpenExchangeRateBackendTestCase(TestCase):

    def test_no_app_id_configured(self):
        currency_settings.OPENEXCHANGE_APP_ID = None
        with self.assertRaises(ImproperlyConfigured):
            OpenExchangeBackend()

    def test_backend_generates_correct_url(self):
        currency_settings.OPENEXCHANGE_APP_ID = 'APP_ID'
        backend = OpenExchangeBackend()
        url = backend.get_end_point_url('AUD', symbols=None)
        self.assertEqual("https://openexchangerates.org/api/latest.json?app_id=APP_ID&base=AUD", url)

    def test_convert_money(self):
        ExchangeRateFactory(rates={
            'AUD': 1.5,
            'EUR': 0.8
        })
        self.assertEqual(convert_money(1, 'USD', 'AUD'), Decimal('1.5'))
        self.assertEqual(convert_money(1.5, 'AUD', 'EUR'), Decimal('0.80'))
