"""
    Admin model for the analytics
"""

from django.contrib import admin
from .models.social_numbers import SocialNumbers
from .models.promotion_numbers import PromotionNumbers
from .django_admin.social_numbers_admin import SocialNumbersAdmin
from .django_admin.promotion_numbers_admin import PromotionNumbersAdmin

admin.site.register(SocialNumbers, SocialNumbersAdmin)
admin.site.register(PromotionNumbers, PromotionNumbersAdmin)