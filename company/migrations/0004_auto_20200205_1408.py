# Generated by Django 2.2.10 on 2020-02-05 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '__first__'),
        ('company', '0003_auto_20200113_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='social_network',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social_network.SocialNetwork'),
        ),
        migrations.AddField(
            model_name='company',
            name='type_of_account',
            field=models.CharField(choices=[('influencer', 'INFLUENCER'), ('company', 'COMPANY')], default='company', max_length=10),
        ),
    ]
