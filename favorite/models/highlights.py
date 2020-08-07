"""
    Model class for highlights
"""

from django.db import models
from promotion.models.promotion import Promotion


class Highlight(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))), unique=True)
    release_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)

    class Meta:
        verbose_name = "Highlight"
        verbose_name_plural = "Highlights"
