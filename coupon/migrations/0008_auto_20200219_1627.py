# Generated by Django 2.2.10 on 2020-02-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0007_coupon_type_of_distribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='type_of_distribution',
            field=models.CharField(choices=[('direct', 'DIRECT'), ('end_promotion', 'END_PROMOTION'), ('live_draw', 'LIVE_DRAW')], default='direct', max_length=20),
        ),
    ]