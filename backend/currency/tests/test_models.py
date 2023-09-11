import random

import pytest
from _decimal import Decimal
from datetime import date, timedelta

from django.db import IntegrityError

from conftest import currency
from currency.models import CurrencyValue, CurrencyDate, CurrencyName


def test_add_one_currency_data(currency):
    currency_value = CurrencyValue.objects.filter(currency_date=currency).first()

    assert currency_value.currency_date.date == currency.date
    assert currency_value.currency_name.code == "EUR"
    assert currency_value.currency_name.name == "euro"


def test_get_value_by_date_range(currency, currency_euro):
    dates = CurrencyDate.objects.filter(date__range=(date.today() - timedelta(days=5), date.today()))
    values = dates.filter(currency_values__currency_name__code="EUR")
    assert len(values) == 2
    assert values.last().currency_values.first().exchange_rate == Decimal("3.50")


def test_add_two_value_for_one_date_and_currency(currency_date, currency_name):
    CurrencyValue.objects.create(exchange_rate=3.47, currency_date=currency_date, currency_name=currency_name)

    with pytest.raises(IntegrityError) as excinfo:
        CurrencyValue.objects.create(exchange_rate=3.33, currency_date=currency_date, currency_name=currency_name)
    assert "UNIQUE constraint failed" in str(excinfo)


def test_multiple_exchange_rate_at_once(currency_date):
    currencies_names = CurrencyName.objects.all()
    currency_name_count = currencies_names.count()
    values = [round(random.uniform(0.01, 15), 6) for _ in range(currency_name_count)]
    currency_values = [
        CurrencyValue(exchange_rate=value, currency_date=currency_date, currency_name=currencies_names[index])
        for index, value in enumerate(values)
    ]
    CurrencyValue.objects.bulk_create(currency_values)

    currency_values_db = CurrencyValue.objects.all().count()

    assert currency_values_db == currency_name_count
    assert CurrencyDate.objects.get(date=currency_date.date).currency_values.count() == currency_name_count
    assert currencies_names.first().currency_values.filter(currency_date=currency_date).count() == 1
