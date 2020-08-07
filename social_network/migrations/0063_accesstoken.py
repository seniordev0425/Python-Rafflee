# Generated by Django 2.2.13 on 2020-06-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0062_auto_20200625_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_access_token', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Access Token',
                'verbose_name_plural': 'Access Tokens',
            },
        ),
    ]
