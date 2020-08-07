"""
    Model class for company
"""

from django.db import models
from account.models.account import MyUser
from social_network.models.social_network import SocialNetwork

TYPE_OF_ACCOUNT = [
    ('influencer', 'INFLUENCER'),
    ('company', 'COMPANY')
]


class Company(models.Model):
    """
        Model Class for company
    """
    id_company = models.IntegerField(null=True)
    description = models.TextField(null=True, max_length=1000)
    company_name = models.CharField(null=False, max_length=50)
    owner = models.ForeignKey(MyUser, related_name="owner", on_delete=models.CASCADE)
    contributors = models.ManyToManyField(MyUser)
    type_of_account = models.CharField(choices=TYPE_OF_ACCOUNT, max_length=10, null=False, default='company')
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE, null=True)
    logo = models.ImageField(upload_to='logo', null=True)
    logo_url = models.CharField(max_length=1000, null=True)
    address = models.CharField(max_length=2064, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=2064, null=True)
    region = models.CharField(max_length=2064, null=True)
    certified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    def get_contributors(self):
        return ",".join([str(p) for p in self.contributors.all()])

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Firms"
        app_label = 'company'
