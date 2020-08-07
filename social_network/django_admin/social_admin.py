"""
    Admin class for the social network table
"""

from django.contrib import admin


class SocialNetworkAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'youtube_channel_url',
        'youtube_channel_id',
        'facebook_page_url',
        'twitter_page_url',
        'instagram_page_url',
        'twitch_channel_url',
        'twitch_channel_id'
    )

    search_fields = ('youtube_channel_url', 'youtube_channel_id', 'facebook_page_url',
                     'twitter_page_url', 'instagram_page_url', 'twitch_channel_id', 'twitch_channel_url')
