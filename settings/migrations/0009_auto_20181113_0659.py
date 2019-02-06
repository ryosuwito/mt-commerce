# Generated by Django 2.0.8 on 2018-11-13 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_auto_20181113_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footerlink',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog_page.Page'),
        ),
        migrations.AlterField(
            model_name='headerlink',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog_page.Page'),
        ),
    ]
