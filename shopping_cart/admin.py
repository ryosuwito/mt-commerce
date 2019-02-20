from django.contrib import admin
from .models import CartItem

class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    
admin.site.register(CartItem, CartItemAdmin)
