# Generated by Django 2.2.12 on 2020-04-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0036_auto_20200430_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersocialaction',
            name='website',
            field=models.BooleanField(default=False),
        ),
    ]
