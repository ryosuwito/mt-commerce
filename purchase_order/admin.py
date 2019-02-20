from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderAdmin(admin.ModelAdmin):
    model = PurchaseOrder
    
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

class PurchaseOrderItemAdmin(admin.ModelAdmin):
    model = PurchaseOrderItem
    
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)