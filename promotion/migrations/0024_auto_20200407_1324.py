# Generated by Django 2.2.11 on 2020-04-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0023_auto_20200402_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='logo_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='campaign_image_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]