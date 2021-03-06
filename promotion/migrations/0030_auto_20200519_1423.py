# Generated by Django 2.2.12 on 2020-05-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0029_promotion_close_promotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_entries', models.IntegerField(default=1)),
                ('website_mandatory', models.BooleanField(default=False)),
                ('video_entries', models.IntegerField(default=1)),
                ('video_mandatory', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='city',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='country',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='physical_promotion',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='street',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='street_number',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='trade_chain',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='zip_code',
        ),
        migrations.AlterField(
            model_name='promotion',
            name='type_of_distribution',
            field=models.CharField(choices=[('raffle', 'RAFFLE'), ('giveaway', 'GIVEAWAY'), ('reward', 'REWARD')], default='direct', max_length=20),
        ),
    ]
