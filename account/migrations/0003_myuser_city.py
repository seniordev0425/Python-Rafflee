# Generated by Django 2.2.9 on 2020-01-17 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200115_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
