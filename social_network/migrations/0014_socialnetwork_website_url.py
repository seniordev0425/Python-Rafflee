# Generated by Django 2.2.11 on 2020-04-14 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0013_auto_20200402_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialnetwork',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
