# Generated by Django 2.2.12 on 2020-06-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20200519_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='lattitude',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='connection',
            name='longitude',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5),
        ),
    ]
