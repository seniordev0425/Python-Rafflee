"""
    Model class for promotion
"""

from django.db import models
from django_countries.fields import CountryField
from company.models.company import Company
from .winnings import Winnings
from account.models import MyUser
from social_network.models import SocialAction
from .categories import Category

TYPE_OF_PROMOTION = [
    ('private', 'PRIVATE'),
    ('public', 'PUBLIC')
]

TYPE_OF_DISTRIBUTION = [
    ('raffle', 'RAFFLE'),
    ('giveaway', 'GIVEAWAY'),
    ('reward', 'REWARD')
]


class Response(models.Model):
    """
        Model class for question
    """
    response = models.CharField(null=False, max_length=200)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    """
        Model class for question
    """
    question = models.CharField(null=False, max_length=200)

    def __str__(self):
        return self.question


class ResponseTemplate(models.Model):
    """
        Model class for question
    """
    response = models.CharField(null=False, max_length=200)

    def __str__(self):
        return self.response


class Poll(models.Model):
    """
        Model class for poll
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ManyToManyField(ResponseTemplate)
    multiple_choices = models.BooleanField(default=False)


class Video(models.Model):
    """
        Model class for video
    """
    url = models.URLField(null=True, blank=True)
    url_mobile = models.URLField(null=True, blank=True)
    video_name = models.CharField(null=False, max_length=50)


class Promotion(models.Model):
    """
        Model Class for promotion
    """
    campaign_image = models.ImageField(upload_to='campaign', null=True, blank=True)
    campaign_image_url = models.CharField(max_length=1000, null=True, blank=True)
    campaign_name = models.CharField(null=False, max_length=50)
    company = models.ForeignKey(Company, related_name="company", on_delete=models.CASCADE, null=True)
    winnings = models.ManyToManyField(Winnings)
    categories = models.ManyToManyField(Category, blank=True)
    participants = models.ManyToManyField(MyUser, blank=True)
    number_of_eligible_people = models.IntegerField(blank=True, null=True)
    number_of_maximum_participants = models.IntegerField(blank=True, null=True)
    number_of_participants = models.IntegerField(default=0)
    description = models.CharField(max_length=50, blank=True)
    long_description = models.CharField(max_length=2048, blank=True)
    type_of_promotion = models.CharField(choices=TYPE_OF_PROMOTION, max_length=10, null=False, default='public')
    type_of_distribution = models.CharField(choices=TYPE_OF_DISTRIBUTION, max_length=20, null=False, default='direct')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    url_website = models.URLField(null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    live_draw = models.BooleanField(default=False, blank=True)
    result_poll = models.ManyToManyField(Response, blank=True)
    release_date = models.DateTimeField(blank=False, null=False)
    social_action = models.ForeignKey(SocialAction, on_delete=models.CASCADE, null=True, blank=True)
    close_promotion = models.BooleanField(default=False, blank=True)
    followers = models.IntegerField(default=0)
    end_date = models.DateTimeField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotion"
        app_label = 'promotion'

    def __str__(self):
        return self.campaign_name
