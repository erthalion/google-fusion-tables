from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
