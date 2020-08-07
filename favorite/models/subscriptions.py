"""
    Model class for subscriptions
"""

from django.db import models
from account.models.account import MyUser
from company.models.company import Company


class Subscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    follow = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
