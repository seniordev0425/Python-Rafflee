"""
    Model class for company
"""

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    """
        Model Class for company
    """
    email = models.EmailField(null=False)
    phone_number = PhoneNumberField(null=False)
    company_name = models.CharField(null=False, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=4096)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
