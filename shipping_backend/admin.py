from django.contrib import admin
from .models import ShippingOrigin

class ShippingOriginAdmin(admin.ModelAdmin):
    model = ShippingOrigin
    
admin.site.register(ShippingOrigin, ShippingOriginAdmin)