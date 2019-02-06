# Generated by Django 2.0.8 on 2018-11-12 09:57

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.CharField(blank=True, default='', max_length=1000)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(db_index=True, default=datetime.datetime.now)),
                ('is_published', models.BooleanField(db_index=True, default=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='user_uploads/featured_images/')),
                ('page_view', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.CharField(blank=True, default='', max_length=1000)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(db_index=True, default=datetime.datetime.now)),
                ('is_published', models.BooleanField(db_index=True, default=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='user_uploads/featured_images/')),
                ('page_view', models.IntegerField(default=0)),
            ],
        ),
    ]
