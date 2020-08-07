"""
    Admin model for the social network
"""

from django.contrib import admin
from .django_admin.social_admin import SocialNetworkAdmin
from .django_admin.social_connection_admin import SocialConnectionAdmin
from .models.social_network import SocialNetwork
from .models.social_connection import SocialConnection
from .models.user_social_action import UserSocialAction
from .models.access_token import AccessToken
from .django_admin.access_token_admin import AccessTokenAdmin
from .django_admin.user_social_action_admin import UserSocialActionAdmin

admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(UserSocialAction, UserSocialActionAdmin)
admin.site.register(SocialConnection, SocialConnectionAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
