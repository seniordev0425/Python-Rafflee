# Generated by Django 2.2.13 on 2020-07-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0043_auto_20200602_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]