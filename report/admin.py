"""
    Admin model for the report
"""

from django.contrib import admin
from .django_admin.report_admin import ReportAdmin
from .models.report import Report

admin.site.register(Report, ReportAdmin)