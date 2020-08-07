"""
    Analytics for the promotion numbers
"""

from django.db import models
from promotion.models import Promotion


class PromotionNumbers(models.Model):
    """
        Model class for promotion numbers
    """
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    click_views = models.IntegerField(default=0)
    click_actions = models.IntegerField(default=0)
    click_participations = models.IntegerField(default=0)
    click_views_total = models.IntegerField(default=0)
    click_actions_total = models.IntegerField(default=0)
    click_participations_total = models.IntegerField(default=0)
    number_of_followers = models.IntegerField(default=0)
    product_benefit_by_view = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    product_benefit_by_action = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    product_benefit_by_participations = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    product_benefit_by_total = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    product_benefit_followers = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promotion number"
        verbose_name_plural = "Promotion numbers"
