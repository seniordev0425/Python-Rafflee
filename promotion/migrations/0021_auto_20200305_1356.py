# Generated by Django 2.2.10 on 2020-03-05 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0020_auto_20200304_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotion.Poll'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='result_poll',
            field=models.ManyToManyField(blank=True, null=True, to='promotion.Response'),
        ),
    ]
