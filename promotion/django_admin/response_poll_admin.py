"""
    Admin class for the poll table
"""

from django.contrib import admin


class ResponsePollAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'response',
        'user',
        'created'
    )

    list_filter = (
        'response',
        'user',
    )

    search_fields = ('user', 'response')
