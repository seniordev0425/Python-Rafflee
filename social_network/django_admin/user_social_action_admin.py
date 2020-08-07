"""
    Admin class for the social network table
"""

from django.contrib import admin


class UserSocialActionAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'user',
        'promotion',
        'facebook_url',
        'facebook_post',
        'facebook_page',
        'youtube_like',
        'youtube_follow',
        'instagram_profile',
        'instagram_publication',
        'twitter_like',
        'twitter_tweet',
        'twitter_retweet',
        'twitter_follow',
        'twitch_follow',
        'poll',
        'video',
        'website',
        'distributed'
    )

    list_filter = (
        'user',
        'promotion',
        'distributed',
    )

    search_fields = ('user', 'promotion', 'distributed')
