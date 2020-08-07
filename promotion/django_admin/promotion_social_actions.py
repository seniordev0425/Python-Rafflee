"""
    Admin class for the social action table
"""

from django.contrib import admin


class SocialActionAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'company_name',
        'campaign_name',
        'facebook_url',
        'facebook_post',
        'facebook_page',
        'youtube_like',
        'youtube_follow',
        'instagram_profile_url',
        'instagram_publication_url',
        'twitter_like',
        'twitter_tweet',
        'twitter_tweet_model',
        'twitter_retweet',
        'twitter_follow',
        'twitch_follow',
        'poll',
        'video',
        'website'
    )
