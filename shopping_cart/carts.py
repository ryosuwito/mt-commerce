from .models import Cart, CartItem, AnonymousCart
from catalog.models import Product

def get_cart(request):
    cart_object =''
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    cart_id = request.session.get('shopping_cart', -1)
    if request.user.is_authenticated:
        try:
            cart_object = request.user.users_cart
        except:
            cart_object = Cart.objects.get_or_create(user=request.user)[0]
            cart_id = cart_object.id
            
    else:
        try:
            cart_object = AnonymousCart.objects.get(id=cart_id)
        except:
            cart_object = AnonymousCart.objects.create(anon_user=request.session.session_key)
            cart_id = cart_object.id

    request.session['shopping_cart'] = cart_id
    return {'cart_object':cart_object,'cart_id':cart_id}
    
def transfer_cart(request, anon_cart):
    user_cart = ''
 
    try:
        user_cart = request.user.users_cart
    except:
        user_cart = Cart.objects.create(user=request.user)

    if anon_cart.get_total_products():
        temp_cart = Cart.objects.get(id=anon_cart.id)
        if not user_cart:
            user_cart = temp_cart
            user_cart.user = request.user
            user_cart.save()
        else:
            for item in temp_cart.get_items_in_cart():
                try:
                    cart_item = CartItem.objects.get(cart=user_cart, 
                            product=item.product)   
                    cart_item.quantity += item.quantity
                except:
                    cart_item = CartItem.objects.create(cart=user_cart, 
                        product=item.product)
                    cart_item.quantity = item.quantity
                cart_item.save()
                item.delete()
            temp_cart.delete()
    elif not user_cart:
        user_cart = Cart.objects.create(user=request.user)

    request.session['shopping_cart'] = -1
    return {'cart_object':user_cart,'cart_id':user_cart.id}