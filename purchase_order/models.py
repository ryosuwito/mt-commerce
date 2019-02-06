from django.db import models
from django.contrib.auth.models import User
from shopping_cart.models import Cart
from catalog.models import Product
from membership.models import Member, Customer

from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, related_name="users_order", on_delete=models.SET_NULL, null=True)
    total_price = models.PositiveIntegerField(null=True, help_text="Total Belanja")
    discount = models.PositiveIntegerField(null=True, help_text="Diskon Member")
    shipping_cost = models.PositiveIntegerField(null=True, help_text="Ongkos Kirim")
    total_payment = models.PositiveIntegerField(null=True, help_text="Total Belanja")
    created_date = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    payment_date = models.DateTimeField(null=True, db_index=True, blank=True)
    #token_expiry_date = models.DateTimeField(null=True, blank=True)
    #is_tokenized = models.BooleanField(db_index=True,default=False)
    #is_token_expired = models.BooleanField(db_index=True,default=False)
    is_verified = models.BooleanField(db_index=True,default=False)
    is_valid = models.BooleanField(db_index=True,default=True)
    is_paid = models.BooleanField(db_index=True,default=False)
    is_checked_out = models.BooleanField(db_index=True,default=False)
    order_number = models.CharField(db_index=True, max_length=20, blank=True)
    alamat_tujuan = models.CharField(max_length=500, blank=True)
    service = models.CharField(max_length=200, blank=True)
    sub_service = models.CharField(max_length=200, blank=True) #done
    #payment_status = models.TextField(blank=True)
    #payment_token = models.CharField(null=True, max_length=50, blank=True)

    is_set_as_dropship = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    def get_number():
        order_number_alpha = get_random_string(5, 
            allowed_chars='0123456789')
        order_number_beta = get_random_string(5, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        order_number = '%s%s'%(order_number_alpha, order_number_beta)
        if PurchaseOrder.objects.filter(order_number= order_number).exists():
            get_number()
        else:
            return 'INV-{}'.format(order_number)

    class Meta:
        verbose_name = "PurchaseOrder"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
       return 'Purchase Order No. : %s'%self.order_number

class PurchaseOrderItem(models.Model):
    quantity = models.PositiveIntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name="product_in_order", on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="item_in_order", on_delete=models.SET_NULL, null=True)
    product_referal = models.ForeignKey(Member, on_delete=models.SET_NULL, db_index=True,  related_name="product_order_referal", null=True, blank=True) 
    is_valid = models.BooleanField(db_index=True,default=True)
    
    class Meta:
        verbose_name_plural = "items in Order"

    def get_item_details(self):
        details = {}
        details['product_details'] = Product.get_details(self.product)
        details['total_weight'] = self.quantity * self.product.unit_weight
        details['subtotal'] = self.quantity * self.product.price
        return details

    def __str__(self):
       return 'CartItem%s'%self.pk

@receiver(post_save, sender=PurchaseOrder)
def create_purchase_order(sender, instance, created, **kwargs):
    if created:
        instance.order_number = PurchaseOrder.get_number()
        instance.save()