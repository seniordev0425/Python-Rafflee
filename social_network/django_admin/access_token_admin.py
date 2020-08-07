"""
    Admin class for the access token
"""

from django.contrib import admin


class AccessTokenAdmin(admin.ModelAdmin):
    """
    Admin class for the access token
    """

    list_display = (
        'twitter_access_token',
    )
