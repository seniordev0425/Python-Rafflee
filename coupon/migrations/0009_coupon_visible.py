# Generated by Django 2.2.10 on 2020-02-19 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0008_auto_20200219_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]