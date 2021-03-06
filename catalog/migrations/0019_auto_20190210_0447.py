# Generated by Django 2.1.5 on 2019-02-10 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_wilayah', '0005_auto_20180911_1541'),
        ('catalog', '0018_auto_20190210_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount_sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='kota',
            field=models.ForeignKey(help_text='Kota Produk', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_in_city', to='database_wilayah.Kota'),
        ),
        migrations.AddField(
            model_name='product',
            name='provinsi',
            field=models.ForeignKey(help_text='Provinsi Produk', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_in_province', to='database_wilayah.Provinsi'),
        ),
    ]
