# Generated by Django 2.0.6 on 2018-07-13 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0013_auto_20180712_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_member_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='referal_code',
            field=models.CharField(blank=True, db_index=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='member',
            name='sponsor_code',
            field=models.CharField(blank=True, db_index=True, max_length=12),
        ),
    ]
