# Generated by Django 2.2.10 on 2020-02-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_channel_url', models.URLField(blank=True, null=True)),
                ('youtube_channel_id', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube_api_id', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube_api_key', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook_page_url', models.URLField(blank=True, null=True)),
                ('facebook_api_id', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook_api_key', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter_page_url', models.URLField(blank=True, null=True)),
                ('twitter_api_id', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter_api_key', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram_page_url', models.URLField(blank=True, null=True)),
                ('instagram_api_id', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram_api_key', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Socials Networks',
                'verbose_name': 'Social Network',
            },
        ),
    ]