from django.contrib import admin
from .models import Brand, Category, Product

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    exclude = ['slug']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ['slug']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    exclude = ['slug']

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)