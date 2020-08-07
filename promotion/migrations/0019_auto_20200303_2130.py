# Generated by Django 2.2.10 on 2020-03-03 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0018_auto_20200303_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='category')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=250)),
                ('activated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.DeleteModel(
            name='Categorie',
        ),
        migrations.AlterField(
            model_name='promotion',
            name='categories',
            field=models.ManyToManyField(to='promotion.Category'),
        ),
    ]
