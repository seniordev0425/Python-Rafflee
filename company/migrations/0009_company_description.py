# Generated by Django 2.2.11 on 2020-04-07 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20200217_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
