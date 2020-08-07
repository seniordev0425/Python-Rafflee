"""
    Admin class for the promotion table
"""

from django.contrib import admin


class PromotionAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion
    """
    list_display = (
        'pk',
        'campaign_name',
        'company',
        'number_of_eligible_people',
        'release_date',
        'end_date',
        'created'
    )

    list_filter = (
        'campaign_name',
        'company',
        'release_date',
        'end_date',
        'created'
    )

    search_fields = ('campaign_name', 'company', 'release_date', 'end_date', 'created')
