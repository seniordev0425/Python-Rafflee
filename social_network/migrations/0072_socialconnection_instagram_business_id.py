# Generated by Django 2.2.13 on 2020-07-09 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0071_auto_20200709_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconnection',
            name='instagram_business_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
