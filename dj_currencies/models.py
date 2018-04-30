# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from dj_currencies.sources import currency_exchange_choices


class ExchangeRate(models.Model):
    source = models.PositiveSmallIntegerField(
        choices=currency_exchange_choices,
        help_text=_('Where the exchange data comes from'),
    )
    base_currency = models.CharField(max_length=3, db_index=True)
    rates = JSONField(default=dict)
    last_updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['base_currency', '-last_updated_at']

    def __repr__(self):
        return 'Exchange rate for {0}'.format(self.base_currency)
