from django.contrib import admin

from . import models

admin.site.register(models.CurrencyValue)
admin.site.register(models.CurrencyName)
admin.site.register(models.CurrencyDate)
