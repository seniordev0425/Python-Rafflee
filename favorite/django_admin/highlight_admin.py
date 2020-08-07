"""
    Admin class for the highlight table
"""

from django.contrib import admin


class HighlightAdmin(admin.ModelAdmin):
    """
    Admin class for the highlight
    """

    list_display = (
        'promotion',
        'release_date',
        'end_date',
        'priority'
    )

    list_filter = (
        'promotion',
        'release_date',
        'end_date',
        'priority'
    )

    search_fields = ('promotion', 'release_date', 'end_date')
