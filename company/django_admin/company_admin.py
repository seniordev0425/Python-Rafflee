"""
    Admin class for the company table
"""

from django.contrib import admin


class CompanyAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'pk',
        'id_company',
        'company_name',
        'owner',
        'get_contributors',
        'social_network',
        'created',
    )

    list_filter = (
        'id_company',
        'owner',
    )

    search_fields = ('campaign_name', 'owner')
