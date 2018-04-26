from django.contrib import admin
from .models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'base_currency',
        'last_updated_at',
    )
    list_filter = ('source', 'base_currency',)
    date_hierarchy = 'last_updated_at'


admin.site.register(ExchangeRate, ExchangeRateAdmin)
