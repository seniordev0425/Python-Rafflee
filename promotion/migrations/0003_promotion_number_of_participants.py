# Generated by Django 2.2.9 on 2020-01-04 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_promotion_type_of_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='number_of_participants',
            field=models.IntegerField(default=0),
        ),
    ]
