"""
    Model class for categories
"""

from django.db import models


class Category(models.Model):
    """
        Model Class for categories
    """

    logo = models.ImageField(upload_to='category', null=True, blank=True)
    logo_url = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(null=False, max_length=50, unique=True)
    description = models.CharField(null=False, max_length=250, blank=True)
    activated = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name