# Generated by Django 2.2.12 on 2020-06-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0057_auto_20200603_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialconnection',
            name='facebook_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='google_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitch_client_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitch_id_token',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitch_refresh_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitch_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitch_user_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_connection_oauth_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_connection_oauth_token_secret',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_oauth_token_data',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialconnection',
            name='twitter_oauth_token_secret',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]