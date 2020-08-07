"""
    Model class for token
"""

from django.db import models
from account.models.account import MyUser
from promotion.models.promotion import Promotion

TYPE_OF_DISTRIBUTION = [
    ('raffle', 'RAFFLE'),
    ('giveaway', 'GIVEAWAY'),
    ('reward', 'REWARD')
]


class Coupon(models.Model):
    """
        Model class for token
    """
    user = models.ForeignKey(MyUser, related_name="user", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=2048, null=True)
    promotion = models.ForeignKey(Promotion, related_name="promotion", on_delete=models.CASCADE, null=True)
    type_of_distribution = models.CharField(choices=TYPE_OF_DISTRIBUTION, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=2048, null=True)
    distributed = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        app_label = 'coupon'
