"""
    Admin class for the poll table
"""

from django.contrib import admin


class PollAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'question',
        'multiple_choices'
    )

    list_filter = (
        'question',
        'multiple_choices'
    )

    search_fields = ('question',)
