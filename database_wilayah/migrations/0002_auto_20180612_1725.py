# Generated by Django 2.0.6 on 2018-06-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_wilayah', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kecamatan',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='kelurahan',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='kota',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='provinsi',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
