from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(db_index=True,
            max_length = 100,
            help_text="Nama Brand")
    slug = AutoSlugField(max_length=100, 
            unique=True, 
            db_index=True,
            populate_from=('name',))
    description = models.TextField(blank=True,
            help_text="Deskripsi Brand")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Kategori") 

    class Meta:
        verbose_name_plural = "Brands"


    def __str__(self):
       return self.name

    def get_url(self):
        return "/store/brand/%s/" % (self.pk)

class Category(models.Model):
    name = models.CharField(db_index=True,
            max_length = 100,
            help_text="Nama Kategori")
    slug = AutoSlugField(max_length=100, 
            unique=True, 
            db_index=True,
            populate_from=('name',))
    description = models.TextField(blank=True,
            help_text="Deskripsi Kategori")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Kategori") 

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
       return self.name

    def get_url(self):
        return "/store/kategori/%s/" % (self.pk)


class Product(models.Model):
    name = models.CharField(max_length = 200,
            db_index=True,
            help_text="Nama Produk")
    slug = AutoSlugField(max_length=100, 
            db_index=True,
            unique=True, 
            populate_from=('name',))
    description = models.TextField(null=True,help_text="Deskripsi Produk")
    summary = models.TextField(null=True,help_text="Ringkasan Produk")
    photo = models.ImageField(upload_to = 'product_photo',
            help_text="Foto Produk")
    photo_alt1 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 1")
    photo_alt2 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 2")
    photo_alt3 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 3")
    photo_alt4 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 4")
    photo_alt5 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 5")
    price = models.PositiveIntegerField(null=True, help_text="Harga Produk", default=0)
    point = models.PositiveIntegerField(null=True, help_text="Poin Produk", default=0)

    unit_weight = models.PositiveIntegerField(null=True, help_text="Berat Satuan Produk dalam gram")
    is_available = models.BooleanField(default = True,
            help_text="Centang Jika Produk Tersedia")
    is_featured = models.BooleanField(default = False,
            help_text="Centang untuk menjadikan unggulan")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Produk")
    categories = models.ManyToManyField(Category, 
            related_name="products_in_category",
            help_text="Kategori Produk")
    brands = models.ForeignKey(Brand, 
            on_delete=models.SET_NULL,
            null=True,
            related_name="products_in_brand",
            help_text="Brand Produk")

    def get_details(self):
        details = {'name': self.name,
                   'weight' : self.unit_weight,
                   'price' : self.price}
        return details

    def get_photo_url(self):
        return "/media/%s" % (self.photo)

    def get_photo_alt1_url(self):
        return "/media/%s" % (self.photo_alt1)
    def get_photo_alt2_url(self):
        return "/media/%s" % (self.photo_alt2)
    def get_photo_alt3_url(self):
        return "/media/%s" % (self.photo_alt3)
    def get_photo_alt4_url(self):
        return "/media/%s" % (self.photo_alt4)
    def get_photo_alt5_url(self):
        return "/media/%s" % (self.photo_alt5)

    def get_detail_url(self):
        return reverse('storefront:product_detail', kwargs={'product_pk':self.pk})

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
       return self.name