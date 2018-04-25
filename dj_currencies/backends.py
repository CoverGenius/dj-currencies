from __future__ import unicode_literals
import logging
import json
from decimal import Decimal

from django.core.exceptions import ImproperlyConfigured
from dj_currencies.sources import CurrencyDataExchangeSource
from .settings import currency_settings

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .exceptions import RateBackendError
from .models import ExchangeRate


logger = logging.getLogger(__name__)


class BaseRateBackend(object):
    def get_latest_rates(self, base_currency=currency_settings.BASE_CURRENCY, symbols=None):
        """
        Fetch latest rates for one base currency
        :param base_currency: a three letter currency symbol
        :param symbols: List of symbols to fetch
        :return:
        """
        raise NotImplementedError()

    def update_rates(self):
        raise NotImplementedError()


class OpenExchangeBackend(BaseRateBackend):

    def __init__(self):
        if not currency_settings.OPENEXCHANGE_APP_ID:
            raise ImproperlyConfigured(
                "OPENEXCHANGE_APP_ID setting should not be empty when using OpenExchangeBackend")

        if not currency_settings.BASE_CURRENCY:
            raise ImproperlyConfigured(
                "BASE_CURRENCY setting should not be empty. It should be set as a three letter currency code")

        # Build the base api url
        self.base_url = 'https://openexchangerates.org/api/latest.json?app_id={0}'.format(
            currency_settings.OPENEXCHANGE_APP_ID
        )

    def get_end_point_url(self, base_currency, symbols):
        url = self.base_url + '&base={0}'.format(base_currency)
        if symbols:
            symbol_args = ','.join(symbols)
            url = url + '&symbols={0}'.format(symbol_args)
        return url

    def get_latest_rates(self, base_currency=currency_settings.BASE_CURRENCY, symbols=None):
        url = self.get_end_point_url(base_currency, symbols)

        try:
            data = urlopen(url).read().decode("utf-8")
            return json.loads(data)['rates']
        except Exception as e:
            logger.exception("Error retrieving data from %s", url)
            raise RateBackendError("Error retrieving rates: %s" % e)

    def update_rates(self):
        rates = self.get_latest_rates(currency_settings.BASE_CURRENCY)
        return ExchangeRate.objects.create(
            base_currency=currency_settings.BASE_CURRENCY,
            rates=rates,
            source=CurrencyDataExchangeSource.OPENEXCHANGERATES,
        )

    def convert_money(self, amount, currency_from, currency_to):
        rate_qs = ExchangeRate.objects.order_by('-last_updated_at')
        if not rate_qs.exists():
            raise RateBackendError('No cached exchange rates, please run ./manage.py update_exchange_rates')
        exchange_rate = rate_qs[0]

        if exchange_rate.base_currency != currency_from:
            rate_from = exchange_rate.rates.get(currency_to)
        else:
            # If currency from is the same as base currency its rate is 1.
            rate_from = Decimal(1)

        if isinstance(amount, float):
            amount = Decimal(amount).quantize(Decimal('.000001'))

        rate_to = exchange_rate.rates.get(currency_to)

        if not rate_to:
            raise RateBackendError(
                'No exchange rate found from {0} to {1}'.format(exchange_rate.base_currency, currency_to))
        converted_amount = (amount / rate_from) * rate_to

        return converted_amount.quantize(Decimal('1.00'))


