"""
    Model class for social connection network settings
"""

from django.db import models


class SocialConnection(models.Model):
    """
        Model Class for Social connection
    """
    facebook_id = models.CharField(null=True, max_length=100, blank=True)
    facebook_login_connected = models.BooleanField(default=False)
    facebook_short_access_token = models.CharField(null=True, max_length=1000, blank=True)
    facebook_long_access_token = models.CharField(null=True, max_length=1000, blank=True)
    facebook_page_access_token = models.CharField(null=True, max_length=1000, blank=True)
    facebook_page_id = models.CharField(null=True, max_length=100, blank=True)
    facebook_rights_connected = models.BooleanField(default=False)
    facebook_page_connected = models.BooleanField(default=False)
    facebook_date_token = models.DateField(null=True, blank=True)
    google_id = models.CharField(null=True, max_length=200, blank=True)
    google_connected = models.BooleanField(default=False)
    twitter_id = models.CharField(null=True, max_length=100, blank=True)
    twitter_connection_oauth_token = models.CharField(null=True, max_length=100, blank=True)
    twitter_connection_oauth_token_secret = models.CharField(null=True, max_length=100, blank=True)
    twitter_oauth_token_data = models.CharField(null=True, max_length=100, blank=True)
    twitter_oauth_token_secret = models.CharField(null=True, max_length=100, blank=True)
    twitter_connected = models.BooleanField(default=False)
    twitch_client_id = models.CharField(null=True, max_length=200, blank=True)
    twitch_user_id = models.CharField(null=True, max_length=200, blank=True)
    twitch_id_token = models.CharField(null=True, max_length=2000, blank=True)
    twitch_token = models.CharField(null=True, max_length=200, blank=True)
    twitch_refresh_token = models.CharField(null=True, max_length=200, blank=True)
    twitch_connected_mobile = models.BooleanField(default=False)
    twitch_connected = models.BooleanField(default=False)
    snapchat_id = models.CharField(null=True, max_length=100, blank=True)
    snapchat_token = models.CharField(null=True, max_length=1000, blank=True)
    snapchat_refresh_token = models.CharField(null=True, max_length=1000, blank=True)
    snapchat_connected = models.BooleanField(default=False)
    instagram_username = models.CharField(null=True, max_length=100, blank=True)
    instagram_id = models.CharField(null=True, max_length=100, blank=True)
    instagram_short_access_token = models.CharField(null=True, max_length=1000, blank=True)
    instagram_long_access_token = models.CharField(null=True, max_length=1000, blank=True)
    instagram_date_token = models.DateField(null=True, blank=True)
    instagram_connected = models.BooleanField(default=False)
    instagram_business_id = models.CharField(null=True, max_length=100, blank=True)
    instagram_business_short_access_token = models.CharField(null=True, max_length=1000, blank=True)
    instagram_business_long_access_token = models.CharField(null=True, max_length=1000, blank=True)
    instagram_business_date_token = models.DateField(null=True, blank=True)
    instagram_business_connected = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Social Connection"
        verbose_name_plural = "Socials Connections"
