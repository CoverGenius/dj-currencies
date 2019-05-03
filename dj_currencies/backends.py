from __future__ import unicode_literals

from decimal import Decimal
import json
import logging
from urllib.request import urlopen

from django.core.exceptions import ImproperlyConfigured

from dj_currencies.sources import CurrencyDataExchangeSource
from .exceptions import RateBackendError
from .models import ExchangeRate
from .settings import currency_settings

logger = logging.getLogger(__name__)


class BaseRateBackend(object):

    def get_latest_rates(self, base_currency, symbols=None):
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

        if not currency_settings.BASE_CURRENCIES:
            raise ImproperlyConfigured(
                "BASE_CURRENCIES setting should not be empty. It should be set as a three letter currency code")

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

    def get_cached_rates(self, symbols=None):
        if not symbols:
            return {}

        ex_rates = ExchangeRate.objects.order_by('base_currency', '-last_updated_at').filter(
            base_currency__in=symbols
        ).distinct('base_currency')[:len(symbols)]

        return {ex_rate.base_currency: ex_rate.rates for ex_rate in ex_rates}

    def get_latest_rates(self, base_currency, symbols=None):
        url = self.get_end_point_url(base_currency, symbols)

        try:
            data = urlopen(url).read().decode("utf-8")
            return json.loads(data)['rates']
        except Exception as e:
            logger.exception("Error retrieving data from %s", url)
            raise RateBackendError("Error retrieving rates: %s" % e)

    def update_rates(self):
        for currency in currency_settings.BASE_CURRENCIES:
            print('Updating exchange rates with base currency {0}'.format(currency))
            rates = self.get_latest_rates(currency)
            ExchangeRate.objects.create(
                base_currency=currency,
                rates=rates,
                source=CurrencyDataExchangeSource.OPENEXCHANGERATES,
            )

    def convert_money(self, amount, currency_from, currency_to):
        ex_rate = ExchangeRate.objects.base_currency(currency_from).within_days(
            currency_settings.MAX_CACHE_DAYS)

        if isinstance(amount, float):
            amount = Decimal(amount).quantize(Decimal('.000001'))

        rate_to = ex_rate.rates.get(currency_to)

        if not rate_to:
            raise RateBackendError(
                'No exchange rate found from {0} to {1}'.format(ex_rate.base_currency, currency_to))
        rate_to = Decimal(str(rate_to)).quantize(Decimal('.000001'))
        converted_amount = amount * rate_to

        return converted_amount.quantize(Decimal('1.00'))
