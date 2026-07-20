from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True, default='')
    category = models.CharField(max_length=50, blank=True, default='')
    supplier = models.CharField(max_length=100, blank=True, default='')
    low_stock_threshold = models.IntegerField(default=5)
    image = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold