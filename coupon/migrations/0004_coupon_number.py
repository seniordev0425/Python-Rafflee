# Generated by Django 2.2.9 on 2020-01-20 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_auto_20200120_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]