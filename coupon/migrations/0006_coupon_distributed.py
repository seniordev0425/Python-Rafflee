# Generated by Django 2.2.9 on 2020-01-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0005_coupon_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='distributed',
            field=models.BooleanField(default=False),
        ),
    ]
