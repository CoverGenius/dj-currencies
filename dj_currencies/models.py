from datetime import timedelta

from django.db import models
from django.db.models.manager import BaseManager
from django.utils.translation import gettext_lazy as _

from dj_currencies.exceptions import RateBackendError
from dj_currencies.sources import currency_exchange_choices
from django.utils.timezone import now


class ExchangeRateQuerySet(models.QuerySet):
    def base_currency(self, base_currency):
        qs = self.filter(base_currency=base_currency)
        if not qs.exists():
            raise RateBackendError(
                f'No exchange rates for base_currency {base_currency} found'
            )
        return qs

    def within_days(self, days):
        days_ago = now() - timedelta(days=days)
        try:
            return self.filter(last_updated_at__gte=days_ago).order_by(
                '-last_updated_at'
            )[0]
        except IndexError:
            raise RateBackendError(
                'No exchange rates found within {} days, '
                'please run ./manage.py update_exchange_rates'.format(days)
            )


class ExchangeRate(models.Model):
    source = models.PositiveSmallIntegerField(
        choices=currency_exchange_choices,
        help_text=_('Where the exchange data comes from'),
    )
    base_currency = models.CharField(max_length=3, db_index=True)
    rates = models.JSONField(default=dict)
    last_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    objects = BaseManager.from_queryset(ExchangeRateQuerySet)()

    class Meta:
        ordering = ['base_currency', '-last_updated_at']

    def __repr__(self):
        return f'Exchange rate for {self.base_currency}'
