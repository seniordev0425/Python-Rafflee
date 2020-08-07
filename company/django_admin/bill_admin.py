"""
    Admin class for the bill table
"""

from django.contrib import admin


class BillAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'company',
        'promotion',
        'price',
        'bill',
        'emission_date'
    )

    list_filter = (
        'company',
        'promotion',
        'price',
        'emission_date'
    )

    search_fields = ('company', 'promotion', 'price', 'emission_date')
