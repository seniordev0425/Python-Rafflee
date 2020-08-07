"""
    Model class for bills
"""

from django.db import models
from .company import Company
from promotion.models.promotion import Promotion


class Bills(models.Model):
    """
        Model class for bills
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    bill = models.FileField(upload_to='bill')
    emission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"