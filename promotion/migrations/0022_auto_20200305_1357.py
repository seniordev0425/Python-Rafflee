# Generated by Django 2.2.10 on 2020-03-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0021_auto_20200305_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='result_poll',
            field=models.ManyToManyField(blank=True, to='promotion.Response'),
        ),
    ]