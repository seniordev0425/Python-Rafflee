"""
    Admin model for the company
"""

from django.contrib import admin
from .django_admin.company_admin import CompanyAdmin
from .django_admin.bill_admin import BillAdmin
from .models.company import Company
from .models.bills import Bills
from .models.contact import Contact
from .django_admin.contact_admin import ContactAdmin

admin.site.register(Company, CompanyAdmin)
admin.site.register(Bills, BillAdmin)
admin.site.register(Contact, ContactAdmin)