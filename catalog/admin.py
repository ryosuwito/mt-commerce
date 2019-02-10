from django.contrib import admin
from .models import Store, Category, Product

class StoreAdmin(admin.ModelAdmin):
    model = Store
    exclude = ['slug']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ['slug']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    exclude = ['slug']

admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)