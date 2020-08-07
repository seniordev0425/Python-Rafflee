# Generated by Django 2.2.13 on 2020-07-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0074_socialconnection_facebook_page_connected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entries',
            old_name='facebook_comment_entries',
            new_name='facebook_page_entries',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='facebook_comment_mandatory',
            new_name='facebook_page_mandatory',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='facebook_follow_entries',
            new_name='facebook_url_entries',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='facebook_follow_mandatory',
            new_name='facebook_url_mandatory',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='facebook_comment',
            new_name='facebook_page',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='facebook_follow',
            new_name='facebook_page_follow',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='facebook_like',
            new_name='facebook_page_share',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='facebook_comment_id',
            new_name='facebook_page_url',
        ),
        migrations.RenameField(
            model_name='socialaction',
            old_name='facebook_like_id',
            new_name='facebook_post_url',
        ),
        migrations.RemoveField(
            model_name='entries',
            name='facebook_like_entries',
        ),
        migrations.RemoveField(
            model_name='entries',
            name='facebook_like_mandatory',
        ),
        migrations.RemoveField(
            model_name='socialaction',
            name='facebook_comment_model',
        ),
        migrations.RemoveField(
            model_name='socialaction',
            name='facebook_post_model',
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_post_comment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_post_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_post_share',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_url',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_url_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_url_share',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialaction',
            name='facebook_url_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
