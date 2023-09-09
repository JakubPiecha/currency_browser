from datetime import date, timedelta

import pytest

from currency.models import CurrencyName, CurrencyDate, CurrencyValue


@pytest.fixture
def currency(db):
    currency_name = CurrencyName.objects.get(code="EUR")
    currency_date = CurrencyDate.objects.create(date=date.today())
    currency_value = CurrencyValue.objects.create(exchange_rate=5.50)
    currency_value.currency_names.add(currency_name)
    currency_value.currency_dates.add(currency_date)
    return currency_date


@pytest.fixture
def currency_euro(db):
    currency_name = CurrencyName.objects.get(code="EUR")
    currency_date = CurrencyDate.objects.create(date=date.today() - timedelta(days=3))
    currency_value = CurrencyValue.objects.create(exchange_rate=3.50)
    currency_value.currency_names.add(currency_name)
    currency_value.currency_dates.add(currency_date)
    return currency_date
