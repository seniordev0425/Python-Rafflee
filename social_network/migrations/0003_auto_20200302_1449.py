# Generated by Django 2.2.10 on 2020-03-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_socialaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialaction',
            name='campaign_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='twitter_follow',
            field=models.BooleanField(default=False),
        ),
    ]
