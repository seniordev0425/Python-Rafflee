"""
    Admin class for the wall settings
"""

from django.contrib import admin

class WallSettings(admin.ModelAdmin):
    """
        Admin class for the connection
    """
    list_display = (
        'facebook',
        'twitter',
        'instagram',
        'id_page_facebook'
    )

    list_filter = (
    )

    search_fields = ()