from django.db import models


class CurrencyRate(models.Model):
    code = models.CharField(max_length=3)
    rate = models.FloatField()
    last_update = models.DateField()
