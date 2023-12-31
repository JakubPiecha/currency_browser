from django.db import models


class CurrencyName(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Currency names"
        verbose_name_plural = "Currency name"


class CurrencyDate(models.Model):
    date = models.DateField(db_index=True, unique=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Currency date"
        verbose_name_plural = "Currency dates"


class CurrencyValue(models.Model):
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=8)
    currency_name = models.ForeignKey("CurrencyName", on_delete=models.CASCADE, related_name="currency_values")
    currency_date = models.ForeignKey("CurrencyDate", on_delete=models.CASCADE, related_name="currency_values")

    def __str__(self):
        return str(self.exchange_rate)

    class Meta:
        verbose_name = "Currency value"
        verbose_name_plural = "Currency values"
        unique_together = ("currency_name", "currency_date")
