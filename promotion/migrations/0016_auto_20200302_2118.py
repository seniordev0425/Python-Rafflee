# Generated by Django 2.2.10 on 2020-03-02 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0015_promotion_campaign_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='campaign_image',
            field=models.ImageField(blank=True, null=True, upload_to='campaign'),
        ),
    ]