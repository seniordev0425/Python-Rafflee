# Generated by Django 2.2.12 on 2020-04-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0028_auto_20200427_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconnection',
            name='google_id_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='google_refresh_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='google_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
