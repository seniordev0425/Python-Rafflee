# Generated by Django 2.2.12 on 2020-04-27 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0027_socialconnection_google_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialaction',
            old_name='twitter_comment',
            new_name='twitter_tweet',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='twitter_comment_model',
            new_name='twitter_tweet_model',
        ),
        migrations.RenameField(
            model_name='usersocialaction',
            old_name='twitter_comment',
            new_name='twitter_tweet',
        ),
    ]