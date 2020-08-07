"""
    Admin class for the contact table
"""

from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    """
    Admin class for the company
    """

    list_display = (
        'email',
        'phone_number',
        'company_name',
        'message',
    )

    list_filter = (
        'email',
    )

    search_fields = ('email', 'phone_number', 'company_name')
