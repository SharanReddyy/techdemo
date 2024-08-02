# stock_data/models.py

from django.db import models

class DailyStock(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.BigIntegerField()
    change_percent = models.FloatField()

    class Meta:
        db_table = 'daily_stock'
        unique_together = ('symbol', 'date')
