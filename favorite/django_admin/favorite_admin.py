"""
    Admin class for the favorite table
"""

from django.contrib import admin


class FavoriteAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'user',
        'promotion',
    )

    list_filter = (
        'user',
        'promotion',
    )

    search_fields = ('user', 'promotion')
