"""
    Model class the the social numbers analytics
"""

from django.db import models
from company.models import Company


class SocialNumbers(models.Model):
    """
        Model class for social numbers
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    twitter_followers = models.IntegerField(default=0)
    instagram_followers = models.IntegerField(default=0)
    facebook_followers = models.IntegerField(default=0)
    snapchat_followers = models.IntegerField(default=0)
    twitch_followers = models.IntegerField(default=0)
    youtube_followers = models.IntegerField(default=0)
    rafflee_followers = models.IntegerField(default=0)
    emission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Social number"
        verbose_name_plural = "Social numbers"
