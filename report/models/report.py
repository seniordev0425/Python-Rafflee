"""
    Model class for reporting
"""

from django.db import models

TYPE_OF_REPORT = [
    ('bug', 'BUG'),
    ('feedback', 'FEEDBACK')
]


class Report(models.Model):
    """
        Model Class for reporting
    """
    context = models.CharField(null=False, max_length=500, blank=True)
    type = models.CharField(choices=TYPE_OF_REPORT, max_length=8, null=False, default='bug')
    description = models.TextField(null=False, max_length=4000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    issue = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

