# Generated by Django 2.2.9 on 2020-01-20 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='expiration_date',
            field=models.DateField(null=True),
        ),
    ]