# Generated by Django 2.0.6 on 2018-07-21 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0005_anonymouswishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='is_checked_out',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='is_expired',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='last_update',
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
