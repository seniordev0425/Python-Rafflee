# Generated by Django 2.2.12 on 2020-06-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0058_auto_20200603_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconnection',
            name='snapchat_connected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='snapchat_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='snapchat_refresh_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='snapchat_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
