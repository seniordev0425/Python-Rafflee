# Generated by Django 2.2.12 on 2020-05-20 16:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotion', '0033_auto_20200519_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]