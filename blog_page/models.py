from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from ckeditor_uploader.fields import RichTextUploadingField

from membership.models import Member

import datetime

class Article(models.Model):
    slug = models.SlugField(max_length=200,unique=True, db_index=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, default="", blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    created_date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    is_published = models.BooleanField(default=True, db_index=True)
    featured_image = models.ImageField(upload_to = 'user_uploads/featured_images/', null=True, blank=True)
    page_view = models.IntegerField(default=0)

    def __str__(self):
        return self.title.title()

    def get_image_url(self):
        return "%s" % ("/media/%s"%self.featured_image)

    def get_url(self):
        return "%s" % ("/blog/%s"%self.slug)
        #return "%s" % (reverse('blog_detail', kwargs={'slug':self.slug}))


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.title.lower())
        while Article.objects.filter(slug = slug).exists():
            slug = slugify("%s-%s"%(instance.title.lower(),get_random_string(5, allowed_chars='12345677890')))

        instance.slug = slug
        instance.save()

class Page(models.Model):
    slug = models.SlugField(max_length=200,unique=True, db_index=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, default="", blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    created_date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    is_published = models.BooleanField(default=True, db_index=True)
    featured_image = models.ImageField(upload_to = 'user_uploads/featured_images/', null=True, blank=True)
    page_view = models.IntegerField(default=0)

    def __str__(self):
        return self.title.title()

    def get_image_url(self):
        return "%s" % ("/media/%s"%self.featured_image)

    def get_url(self):
        return "%s" % ("/page/%s"%self.slug)
        #return "%s" % (reverse('page_detail', kwargs={'slug':self.slug}))


@receiver(post_save, sender=Page)
def create_page(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.title.lower())
        while Page.objects.filter(slug = slug).exists():
            slug = slugify("%s-%s"%(instance.title.lower(),get_random_string(5, allowed_chars='12345677890')))

        instance.slug = slug
        instance.save()