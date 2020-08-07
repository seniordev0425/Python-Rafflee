"""
    Admin class for the report table
"""

from django.contrib import admin


class ReportAdmin(admin.ModelAdmin):
    """
    Admin class for the report
    """
    list_display = (
        'type',
        'context',
        'issue',
        'created'
    )

    list_filter = (
        'type',
    )

    search_fields = ('context',)
