from dj_currencies.models import ExchangeRate
import factory


class ExchangeRateFactory(factory.DjangoModelFactory):
    class Meta:
        model = ExchangeRate

    source = 0
    base_currency = 'USD'
    rates = {
        'AUD': 1.32099,
        'CNY': 6.3277,
        'GBP': 0.717582,
        "USD": 1,
        "EUR": 0.821696
    }
