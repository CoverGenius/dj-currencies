from .settings import currency_settings


def convert_money(amount, currency_from, currency_to):
    backend = currency_settings.DEFAULT_BACKEND()
    return backend.convert_money(amount, currency_from, currency_to)

