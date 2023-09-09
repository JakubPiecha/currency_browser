from _decimal import Decimal
from datetime import date, timedelta

from conftest import currency
from currency.models import CurrencyValue, CurrencyDate


def test_add_one_currency_data(currency):
    currency_value = CurrencyValue.objects.filter(currency_dates=currency).first()

    assert currency_value.currency_dates.first().date == currency.date
    assert currency_value.currency_names.first().code == "EUR"
    assert currency_value.currency_names.first().name == "euro"


def test_get_value_by_date_range(currency, currency_euro):
    dates = CurrencyDate.objects.filter(date__range=(date.today() - timedelta(days=5), date.today()))
    values = dates.filter(currency_values__currency_names__code="EUR")

    assert len(values) == 2
    assert values.last().currency_values.first().exchange_rate == Decimal("3.50")
