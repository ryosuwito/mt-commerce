from django.db import models
from catalog.models import Product
from membership.models import Member#, Customer
from django.contrib.auth.models import User
import datetime

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users_cart", null=True)
    shipping_address = models.CharField(max_length=500, blank=True)
    shipping_cost = models.PositiveIntegerField(null=True, blank=True)
    shipping_service =  models.CharField(max_length = 200,null=True)
    shipping_sub_service =  models.CharField(max_length = 200,null=True)
    #user = models.ForeignKey(User, related_name="users_cart", on_delete=models.SET_NULL, null=True)
    #created_date = models.DateTimeField(default=datetime.datetime.now)
    #last_update = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    #is_expired = models.BooleanField(db_index=True,default=False)
    #is_checked_out = models.BooleanField(db_index=True,default=False)
    #is_paid = models.BooleanField(db_index=True,default=False)
    

    is_set_as_dropship = models.BooleanField(default=False)
    #customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Carts"

    def __str__(self):
       return 'Cart%s'%self.pk 
       from .models import CartItem

    def get_total_items_in_cart(self): #cart object
        try :
            return sum([ i.quantity for i in self.get_items_in_cart()])
        except:
            pass
        return 0                
         
    def get_total_price(self): #cart object
        try :
            return sum([ i.quantity * i.product.price for i in self.get_items_in_cart()])
        except:
            pass
        return 0

         
    def get_total_weight(self): #cart object
        try :
            return sum([ i.quantity * i.product.unit_weight for i in self.get_items_in_cart()])
        except:
            pass
        return 0

    def get_total_products(self):
        return self.get_total_items_in_cart()

    def get_total_prices(self):
        return self.get_total_price()

    def get_items_in_cart(self):   
        return self.item_in_cart.all()

    def get_product_details(self):
        product_details = [x.get_item_details()  for x in self.get_items_in_cart()]
        return product_details

class CartItem(models.Model) :
    quantity = models.PositiveIntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name="product_in_cart", on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, related_name="item_in_cart", on_delete=models.SET_NULL, null=True)
    product_referal = models.ForeignKey(Member, on_delete=models.SET_NULL, db_index=True,  related_name="product_cart_referal", null=True, blank=True) 
    class Meta:
        verbose_name_plural = "Cart items"

    def get_item_details(self):
        details = {}
        details['product_details'] = Product.get_details(self.product)
        details['total_weight'] = self.quantity * self.product.unit_weight
        details['subtotal'] = self.quantity * self.product.price
        return details

    def __str__(self):
       return 'CartItem%s'%self.pk

class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users_wishlist", null=True)
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_total_products(self):
        return len(self.get_items_in_wishlist())

    def get_items_in_wishlist(self):
        return self.item_in_wishlist.all()


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList,  related_name="item_in_wishlist", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name="product_in_wishlist", on_delete=models.SET_NULL, null=True)

class AnonymousCart(Cart):
    anon_user = models.CharField(max_length = 200,
            db_index=True,
            help_text="Nama Anon")

class AnonymousWishlist(WishList):
    anon_user = models.CharField(max_length = 200,db_index=True,help_text="Nama Anon")