# Generated by Django 2.2.10 on 2020-02-28 11:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0009_auto_20200228_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
