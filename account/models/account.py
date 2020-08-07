"""
    Model class for user
"""

import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from social_network.models.social_connection import SocialConnection

GENDER = [
    ('male', 'MALE'),
    ('female', 'FEMALE')
]


class Wall(models.Model):
    """
        Model class for wall settings
    """
    facebook = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)
    instagram = models.BooleanField(default=False)
    id_page_facebook = models.CharField(null=True, blank=True, max_length=200)


class MyUser(AbstractUser):
    """
        Model Class for user
    """
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    phone_number_verification = models.BooleanField(default=False)
    company_account = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=10, blank=True)
    profile_picture = models.ImageField(null=True, upload_to='images', blank=True)
    profile_picture_url = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=2064, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2064, null=True, blank=True)
    region = models.CharField(max_length=2064, null=True, blank=True)
    social_connection = models.ForeignKey(SocialConnection, on_delete=models.CASCADE, null=True)
    settings_wall = models.ForeignKey(Wall, on_delete=models.CASCADE, null=True)
    jwt_secret = models.UUIDField(default=uuid.uuid4)
    last_logout = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        app_label = 'account'
