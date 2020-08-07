"""
    Model class for social network settings
"""

from django.db import models


class SocialNetwork(models.Model):
    """
        Model Class for Social network
    """
    youtube_channel_url = models.URLField(null=True, max_length=200, blank=True)
    youtube_channel_id = models.CharField(null=True, max_length=200, blank=True)
    youtube_api_id = models.CharField(null=True, max_length=200, blank=True)
    youtube_api_key = models.CharField(null=True, max_length=200, blank=True)
    facebook_page_url = models.URLField(null=True, max_length=200, blank=True)
    facebook_api_id = models.CharField(null=True, max_length=200, blank=True)
    facebook_api_key = models.CharField(null=True, max_length=200, blank=True)
    twitter_page_url = models.URLField(null=True, max_length=200, blank=True)
    twitter_api_id = models.CharField(null=True, max_length=200, blank=True)
    twitter_api_key = models.CharField(null=True, max_length=200, blank=True)
    instagram_page_url = models.URLField(null=True, max_length=200, blank=True)
    instagram_api_id = models.CharField(null=True, max_length=200, blank=True)
    instagram_api_key = models.CharField(null=True, max_length=200, blank=True)
    twitch_channel_id = models.CharField(null=True, max_length=200, blank=True)
    twitch_channel_url = models.URLField(null=True, max_length=200, blank=True)
    website_url = models.URLField(null=True, max_length=200, blank=True)

    class Meta:
        verbose_name = "Social Network"
        verbose_name_plural = "Socials Networks"
