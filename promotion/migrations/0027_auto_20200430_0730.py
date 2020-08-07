# Generated by Django 2.2.12 on 2020-04-30 07:30

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0026_promotion_url_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='logo',
            field=models.ImageField(null=True, upload_to='category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='logo_url',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='campaign_image',
            field=models.ImageField(null=True, upload_to='campaign'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='campaign_image_url',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='city',
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='promotion.Poll'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='result_poll',
            field=models.ManyToManyField(to='promotion.Response'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='street',
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='street_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='trade_chain',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='url_website',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='promotion.Video'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='zip_code',
            field=models.IntegerField(null=True),
        ),
    ]