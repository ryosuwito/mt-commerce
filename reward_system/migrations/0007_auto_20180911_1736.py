# Generated by Django 2.0.6 on 2018-09-11 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reward_system', '0006_reward_bonus_selling'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reward',
            old_name='bonus_selling',
            new_name='bonus_purchasing',
        ),
        migrations.RenameField(
            model_name='reward',
            old_name='current_selling',
            new_name='current_purchasing',
        ),
    ]
