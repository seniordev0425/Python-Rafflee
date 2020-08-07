"""
    Admin class for the connection table
"""

from django.contrib import admin

class ConnectionAdmin(admin.ModelAdmin):
    """
        Admin class for the connection
    """
    list_display = (
        'user',
        'ip',
        'device_id',
        'country_name',
        'city_name',
        'continent_name',
        'postal_code',
        'region',
        'emission_date'
    )

    list_filter = (
        'user',
        'device_id',
        'country_name',
        'city_name',
        'continent_name',
        'postal_code',
        'region',
    )

    search_fields = ('user', 'ip', 'device_id', 'emission_date',
                     'country_name', 'city_name', 'continent_name', 'postal_code', 'region')