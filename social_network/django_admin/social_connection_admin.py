"""
    Admin class for the social network table
"""

from django.contrib import admin


class SocialConnectionAdmin(admin.ModelAdmin):
    """
    Admin class for the social connection admin
    """

    list_display = (
        'facebook_login_connected',
        'facebook_rights_connected',
        'twitter_connected',
        'google_connected',
        'twitch_connected',
        'instagram_connected',
        'instagram_business_connected'
    )
