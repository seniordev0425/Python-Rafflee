"""
    Admin class for coupon table
"""

from django.contrib import admin


class CouponAdmin(admin.ModelAdmin):
    """
    Admin class for the coupon
    """
    list_display = (
        'pk',
        'promotion',
        'user',
        'name',
        'promotion',
        'description',
        'visible',
        'distributed',
        'created',
    )

    list_filter = (
        'user',
        'promotion',
    )

    search_fields = ('user', 'promotion')
