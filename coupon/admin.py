"""
    Admin model for coupons
"""

from django.contrib import admin
from .django_admin.coupon_admin import CouponAdmin
from .models.coupon import Coupon

admin.site.register(Coupon, CouponAdmin)

