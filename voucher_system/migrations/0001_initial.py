# Generated by Django 2.0.8 on 2018-11-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Nama Voucher', max_length=200)),
                ('voucher_code', models.CharField(blank=True, db_index=True, help_text='Kode Voucher', max_length=12)),
                ('benefit', models.PositiveSmallIntegerField(choices=[(0, 'Diskon Produk'), (1, 'Diskon Ongkir'), (2, 'Persen Diskon Produk'), (3, 'Persen Diskon Ongkir'), (4, 'Bonus Poin'), (5, 'Cashback Pembelian')], default=0, help_text='Keuntungan Voucher')),
                ('condition', models.PositiveSmallIntegerField(choices=[(6, 'Minimal Pembelian'), (7, 'Batas Maksimal Keuntungan')], default=6, help_text='Syarat & Kondisi Voucher')),
                ('value', models.PositiveIntegerField(default=0, help_text='Nilai Keuntungan Voucher')),
                ('threshold', models.PositiveIntegerField(default=0, help_text='Nilai Syarat & Kondisi Voucher')),
            ],
        ),
    ]
