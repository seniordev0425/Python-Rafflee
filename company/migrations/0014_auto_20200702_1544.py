# Generated by Django 2.2.13 on 2020-07-02 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20200702_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='settings_wall',
        ),
        migrations.DeleteModel(
            name='Wall',
        ),
    ]
