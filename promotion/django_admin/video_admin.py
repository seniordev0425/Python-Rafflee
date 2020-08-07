"""
    Admin class for the video table
"""

from django.contrib import admin


class VideoAdmin(admin.ModelAdmin):
    """
    Admin class for the video
    """
    list_display = (
        'url',
        'video_name',
    )