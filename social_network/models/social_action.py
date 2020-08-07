"""
    Model class for social action
"""

from django.db import models

TYPE_OF_ID = [
    ('user_id', 'USER_ID'),
    ('screen_name', 'SCREEN_NAME')
]

class Entries(models.Model):
    """
        Model class for entries
    """
    website_entries = models.IntegerField(default=1)
    website_mandatory = models.BooleanField(default=False)
    video_entries = models.IntegerField(default=1)
    video_mandatory = models.BooleanField(default=False)
    pool_entries = models.IntegerField(default=1)
    pool_mandatory = models.BooleanField(default=False)
    facebook_post_entries = models.IntegerField(default=1)
    facebook_post_mandatory = models.BooleanField(default=False)
    facebook_url_entries = models.IntegerField(default=1)
    facebook_url_mandatory = models.BooleanField(default=False)
    facebook_page_entries = models.IntegerField(default=1)
    facebook_page_mandatory = models.BooleanField(default=False)
    youtube_like_entries = models.IntegerField(default=1)
    youtube_like_mandatory = models.BooleanField(default=False)
    youtube_follow_entries = models.IntegerField(default=1)
    youtube_follow_mandatory = models.BooleanField(default=False)
    instagram_profile_entries = models.IntegerField(default=1)
    instagram_profile_mandatory = models.BooleanField(default=False)
    instagram_publication_entries = models.IntegerField(default=1)
    instagram_publication_mandatory = models.BooleanField(default=False)
    twitter_like_entries = models.IntegerField(default=1)
    twitter_like_mandatory = models.BooleanField(default=False)
    twitter_follow_entries = models.IntegerField(default=1)
    twitter_follow_mandatory = models.BooleanField(default=False)
    twitter_retweet_entries = models.IntegerField(default=1)
    twitter_retweet_mandatory = models.BooleanField(default=False)
    twitter_tweet_entries = models.IntegerField(default=1)
    twitter_tweet_mandatory = models.BooleanField(default=False)
    twitch_follow_entries = models.IntegerField(default=1)
    twitch_follow_mandatory = models.BooleanField(default=False)


class SocialAction(models.Model):
    """
        Model Class for Social action
    """
    company_name = models.CharField(null=True, max_length=50)
    campaign_name = models.CharField(null=True, max_length=50)
    entries = models.ForeignKey(Entries, related_name="Entries", on_delete=models.CASCADE, default=None)
    facebook_url = models.BooleanField(default=False)
    facebook_url_like = models.BooleanField(default=False)
    facebook_url_share = models.BooleanField(default=False)
    facebook_url_url = models.CharField(null=True, max_length=200, blank=True)
    facebook_post_url = models.CharField(null=True, max_length=200, blank=True)
    facebook_post = models.BooleanField(default=False)
    facebook_post_like = models.BooleanField(default=False)
    facebook_post_comment = models.BooleanField(default=False)
    facebook_post_share = models.BooleanField(default=False)
    facebook_page = models.BooleanField(default=False)
    facebook_page_follow = models.BooleanField(default=False)
    facebook_page_share = models.BooleanField(default=False)
    facebook_page_url = models.CharField(null=True, max_length=200, blank=True)
    youtube_like = models.BooleanField(default=False)
    youtube_follow = models.BooleanField(default=False)
    instagram_profile = models.BooleanField(default=False)
    instagram_profile_url = models.URLField(null=True, max_length=200, blank=True)
    instagram_publication = models.BooleanField(default=False)
    instagram_publication_url = models.URLField(null=True, max_length=200, blank=True)
    twitter_like = models.BooleanField(default=False)
    twitter_like_id = models.CharField(null=True, max_length=100, blank=True)
    twitter_tweet = models.BooleanField(default=False)
    twitter_tweet_model = models.CharField(null=True, max_length=500, blank=True)
    twitter_retweet = models.BooleanField(default=False)
    twitter_retweet_id = models.CharField(null=True, max_length=100, blank=True)
    twitter_follow = models.BooleanField(default=False)
    twitter_follow_type = models.CharField(choices=TYPE_OF_ID, max_length=15, null=True, blank=True)
    twitter_follow_id = models.CharField(null=True, max_length=100, blank=True)
    twitch_follow = models.BooleanField(default=False)
    twitch_follow_name = models.CharField(null=True, max_length=100, blank=True)
    poll = models.BooleanField(default=False)
    website = models.BooleanField(default=False)
    website_url = models.URLField(null=True, blank=True)
    video = models.BooleanField(default=False)
    video_url = models.URLField(null=True, blank=True)
    video_mobile = models.BooleanField(default=False)
    video_url_mobile = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Social Action"
        verbose_name_plural = "Socials Actions"
