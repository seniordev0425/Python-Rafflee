"""
    Admin model for the promotion
"""

from django.contrib import admin
from .django_admin.promotion_admin import PromotionAdmin
from .django_admin.winnings_admin import WinningsAdmin
from .django_admin.poll_admin import PollAdmin
from .django_admin.response_poll_admin import ResponsePollAdmin
from .django_admin.promotion_social_actions import SocialActionAdmin
from .django_admin.categorie_admin import CategoryAdmin
from .django_admin.video_admin import VideoAdmin
from .models.promotion import Promotion, Poll, Response, Video
from .models.winnings import Winnings
from .models.categories import Category
from social_network.models import SocialAction


admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Winnings, WinningsAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Response, ResponsePollAdmin)
admin.site.register(SocialAction, SocialActionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)