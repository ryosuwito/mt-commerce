from .models import WishList, WishListItem, AnonymousWishlist


def get_wishlist(request):
    wishlist_object =''
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    wishlist_id = request.session.get('wishlist', -1)
    if request.user.is_authenticated:
        try:
            wishlist_object = request.user.users_wishlist
        except:
            wishlist_object = WishList.objects.create(user=request.user)
            
    else:
        try:
            wishlist_object = AnonymousWishlist.objects.get(id=wishlist_id)
        except:
            wishlist_object = AnonymousWishlist.objects.create(anon_user=request.session.session_key)
            wishlist_id = wishlist_object.id

    request.session['wishlist'] = wishlist_id
    return {'wishlist_object':wishlist_object,'wishlist_id':wishlist_id}
  
def transfer_wishlist(request, anon_wishlist):
    user_wishlist = ''
 
    try:
        user_wishlist  = request.user.users_wishlist 
    except:
        pass

    if anon_wishlist.get_total_products():
        temp_wishlist = WishList.objects.get(id=anon_wishlist.id)
        if not user_wishlist:
            user_wishlist = temp_wishlist
            user_wishlist.user = request.user
            user_wishlist.save()
        else:
            for item in temp_wishlist.get_items_in_wishlist():
                try:
                    wishlist_item = WishListItem.objects.get(wishlist=user_wishlist, 
                            product=item.product)  
                except:
                    wishlist__item = WishListItem.objects.create(wishlist=user_wishlist, 
                        product=item.product)
                wishlist__item.save()
                item.delete()
            temp_wishlist.delete()
    elif not user_wishlist:
        user_wishlist = WishList.objects.create(user=request.user)

    request.session['wishlist'] = -1
    return {'wishlist_object':user_wishlist,'wishlist_id':user_wishlist.id}