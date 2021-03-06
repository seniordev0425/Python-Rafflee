# Generated by Django 2.2.10 on 2020-02-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0005_auto_20200219_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winnings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winnings_name', models.CharField(max_length=50)),
                ('number_of_eligible_people', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=2048)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Winnings',
                'verbose_name': 'Winning',
            },
        ),
        migrations.AddField(
            model_name='promotion',
            name='winnings',
            field=models.ManyToManyField(to='promotion.Winnings'),
        ),
    ]
