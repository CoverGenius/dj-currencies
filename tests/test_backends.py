from __future__ import unicode_literals
from decimal import Decimal
from django.core.exceptions import ImproperlyConfigured
from django.test import TransactionTestCase
from dj_currencies.apis import convert_money
from dj_currencies.backends import OpenExchangeBackend
from dj_currencies.exceptions import RateBackendError
from dj_currencies.factory import ExchangeRateFactory
from dj_currencies.settings import currency_settings


class OpenExchangeRateBackendTestCase(TransactionTestCase):

    def test_no_app_id_configured(self):
        currency_settings.OPENEXCHANGE_APP_ID = None
        with self.assertRaises(ImproperlyConfigured):
            OpenExchangeBackend()

    def test_backend_generates_correct_url(self):
        currency_settings.OPENEXCHANGE_APP_ID = 'APP_ID'
        backend = OpenExchangeBackend()
        url = backend.get_end_point_url('AUD', symbols=None)
        self.assertEqual("https://openexchangerates.org/api/latest.json?app_id=APP_ID&base=AUD", url)

    def test_convert_money_has_rates(self):
        ExchangeRateFactory(rates={
            'AUD': 1.5,
            'EUR': 0.8
        }, base_currency='USD')
        self.assertEqual(convert_money(1, 'USD', 'AUD'), Decimal('1.5'))

    def test_convert_money_no_rates(self):
        ExchangeRateFactory(rates={
            'USD': 0.75,
        }, base_currency='AUD')
        with self.assertRaises(RateBackendError):
            self.assertEqual(convert_money(1, 'USD', 'AUD'), Decimal('1.5'))
