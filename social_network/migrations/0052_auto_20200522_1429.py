# Generated by Django 2.2.12 on 2020-05-22 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0051_auto_20200519_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_api_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_page_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_api_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_page_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitch_channel_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitch_channel_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_api_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_page_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_api_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_channel_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_channel_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
