"""
    Admin class for the user table
"""

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_staff', 'company_account', 'phone_number_verification')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_active', 'phone_number_verification')}),
        ('Personal info', {'fields': ('profile_picture', 'email', 'first_name', 'last_name', 'date_of_birth',
                                      'phone_number', 'address', 'city', 'country', 'region', 'gender')}),
        ('Permissions', {'fields': ('settings_wall', 'social_connection', 'is_staff', 'company_account', 'last_login', 'last_logout',
                                    'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': 'email',
        }),
    )

    list_filter = (
        'is_staff',
        'company_account',
        'phone_number_verification'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name', 'country')
    ordering = ('date_joined',)
    filter_horizontal = ()
