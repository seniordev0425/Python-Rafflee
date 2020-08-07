# Generated by Django 2.2.12 on 2020-05-11 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0012_auto_20200430_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNumbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_followers', models.IntegerField(default=0)),
                ('instagram_followers', models.IntegerField(default=0)),
                ('facebook_followers', models.IntegerField(default=0)),
                ('snapchat_followers', models.IntegerField(default=0)),
                ('twitch_followers', models.IntegerField(default=0)),
                ('youtube_followers', models.IntegerField(default=0)),
                ('emission_date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
            options={
                'verbose_name_plural': 'Social numbers',
                'verbose_name': 'Social number',
            },
        ),
    ]