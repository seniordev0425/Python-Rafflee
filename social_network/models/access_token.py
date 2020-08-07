"""
    Model class for access_token for rafflee app
"""

from django.db import models


class AccessToken(models.Model):
    """
        Model Class for access token
    """
    twitter_access_token = models.CharField(null=True, max_length=1000)

    class Meta:
        verbose_name = "Access Token"
        verbose_name_plural = "Access Tokens"
