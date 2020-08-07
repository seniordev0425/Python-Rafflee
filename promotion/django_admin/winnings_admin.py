"""
    Admin class for the promotion table
"""

from django.contrib import admin


class WinningsAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'name',
        'number_of_eligible_people',
        'description',
        'created'
    )

    list_filter = (
    )

    search_fields = ('name', 'number_of_eligible_people', 'created')
