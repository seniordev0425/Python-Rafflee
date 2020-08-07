"""
    Admin class for the subscription table
"""

from django.contrib import admin


class SubscriptionsAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'user',
        'company',
        'follow',
        'newsletter'
    )

    list_filter = (
        'user',
        'company',
        'follow',
        'newsletter'
    )

    search_fields = ('user', 'company')
