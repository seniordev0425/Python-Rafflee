# Generated by Django 2.2.12 on 2020-05-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0040_auto_20200511_0815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialconnection',
            name='google_id_token',
        ),
        migrations.RemoveField(
            model_name='socialconnection',
            name='google_refresh_token',
        ),
        migrations.RemoveField(
            model_name='socialconnection',
            name='google_token',
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='facebook_connected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='google_connected',
            field=models.BooleanField(default=False),
        ),
    ]
