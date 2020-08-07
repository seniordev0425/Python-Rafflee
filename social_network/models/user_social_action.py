"""
    Model class for user social action
"""

from django.db import models
from promotion.models import Promotion
from account.models import MyUser


class UserSocialAction(models.Model):
    """
        Model Class for User Social Action
    """
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    facebook_url = models.BooleanField(default=False)
    facebook_post = models.BooleanField(default=False)
    facebook_page = models.BooleanField(default=False)
    youtube_like = models.BooleanField(default=False)
    youtube_follow = models.BooleanField(default=False)
    instagram_publication = models.BooleanField(default=False)
    instagram_profile = models.BooleanField(default=False)
    twitter_like = models.BooleanField(default=False)
    twitter_tweet = models.BooleanField(default=False)
    twitter_retweet = models.BooleanField(default=False)
    twitter_follow = models.BooleanField(default=False)
    twitch_follow = models.BooleanField(default=False)
    poll = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    website = models.BooleanField(default=False)
    entries = models.IntegerField(default=0)
    distributed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User social action"
        verbose_name_plural = "User socials actions"
