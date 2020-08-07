"""
    Admin class for the social numbers analytics table
"""

from django.contrib import admin


class SocialNumbersAdmin(admin.ModelAdmin):
    """
    Admin class for the social numbers analytics
    """

    list_display = (
        'company',
        'rafflee_followers',
        'twitter_followers',
        'instagram_followers',
        'facebook_followers',
        'snapchat_followers',
        'twitch_followers',
        'youtube_followers',
        'emission_date'
    )

    list_filter = (
        'company',
        'emission_date'
    )

    search_fields = ('company',)