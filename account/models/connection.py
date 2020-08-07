"""
    Connection class
"""

from django.db import models
from .account import MyUser

class Connection(models.Model):
    """
        Model class for connection
    """
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField(null=True)
    device_id = models.CharField(max_length=200, null=True)
    country_name = models.CharField(max_length=50, null=True)
    city_name = models.CharField(max_length=50, null=True)
    continent_name = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    latitude = models.DecimalField(default=0, max_digits=13, decimal_places=8)
    longitude = models.DecimalField(default=0, max_digits=13, decimal_places=8)
    emission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connections"