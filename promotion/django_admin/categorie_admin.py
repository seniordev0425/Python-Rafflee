"""
    Admin class for the categorie table
"""

from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'name',
        'activated',
        'created'
    )

    list_filter = (
        'activated',
    )

    search_fields = ('name',)
