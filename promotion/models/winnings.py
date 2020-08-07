"""
    Model class for winnings
"""

from django.db import models


class Winnings(models.Model):
    """
        Model Class for winnings
    """
    name = models.CharField(null=False, max_length=50)
    number_of_eligible_people = models.IntegerField(default=0)
    image = models.ImageField(upload_to='winning', null=True)
    image_url = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Winning"
        verbose_name_plural = "Winnings"

    def __str__(self):
        return self.name
