from django.db import models
from blog_page.models import Page

class FooterLink(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True)
    is_left = models.BooleanField(default=True)
    addr = models.CharField(max_length=400, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name.title()

class HeaderLink(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True)
    pos = models.PositiveIntegerField(null=True, unique=True)
    addr = models.CharField(max_length=400, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name.title()

class HomeLink(models.Model):
    addr_1 = models.CharField(max_length=400, default='/')
    addr_2 = models.CharField(max_length=400, default='/')
    addr_3 = models.CharField(max_length=400, default='/')
    addr_4 = models.CharField(max_length=400, default='/')
    addr_5 = models.CharField(max_length=400, default='/')
    addr_sidebar = models.CharField(max_length=400, default='/')
    addr_middle = models.CharField(max_length=400, default='/')
    banner_1 = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner 1")
    banner_2 = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner 2")
    banner_3 = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner 3")
    banner_4 = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner 4")
    banner_5 = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner 5")
    
    banner_sidebar = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner Sidebar")

    banner_middle = models.ImageField(upload_to = 'home_settings', null=True,
            help_text="Banner Middle")