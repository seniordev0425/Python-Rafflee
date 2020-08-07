# Generated by Django 2.2.12 on 2020-04-30 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0035_auto_20200429_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialconnection',
            name='facebook_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='google_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='google_id_token',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='google_refresh_token',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='google_token',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_connection_oauth_token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_connection_oauth_token_secret',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_oauth_token_data',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_oauth_token_secret',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_api_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_api_key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_page_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_api_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_api_key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_page_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_api_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_api_key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='twitter_page_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='website_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_api_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_api_key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_channel_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='youtube_channel_url',
            field=models.URLField(null=True),
        ),
    ]
