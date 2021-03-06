# Generated by Django 2.2.12 on 2020-06-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20200605_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionnumbers',
            name='product_benefit_by_action',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='promotionnumbers',
            name='product_benefit_by_participations',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='promotionnumbers',
            name='product_benefit_by_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='promotionnumbers',
            name='product_benefit_by_view',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
