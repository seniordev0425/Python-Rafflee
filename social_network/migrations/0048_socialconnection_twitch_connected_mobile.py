# Generated by Django 2.2.12 on 2020-05-15 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0047_auto_20200511_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconnection',
            name='twitch_connected_mobile',
            field=models.BooleanField(default=False),
        ),
    ]
