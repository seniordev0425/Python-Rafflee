"""
    Model class for favorites
"""

from django.db import models
from account.models.account import MyUser
from promotion.models.promotion import Promotion


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
