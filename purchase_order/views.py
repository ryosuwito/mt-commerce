from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from shopping_cart.models import Cart, CartItem, WishListItem
import shopping_cart.carts as carts
import shopping_cart.wishlists as wishlists
from membership.models import Member#, Customer
from shipping_backend.shipping_check import get_courier, get_cost
from django.middleware.csrf import get_token
from shipping_backend.models import ShippingOrigin
from django.forms.models import model_to_dict
from .models import PurchaseOrder, PurchaseOrderItem
from membership.templatetags.int_to_rupiah import int_to_rupiah
from django.urls import reverse
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan
from reward_system.my_point import count_point
from reward_system.my_purchasing import check_purchasing_bonus
#from membership.forms import CustomerAddForm
from settings.models import HeaderLink, FooterLink
import datetime

@login_required
def index(request):
    # if not request.user.member.is_email_verified:
    #     return HttpResponseRedirect(reverse('membership:verify'))
    header_links = HeaderLink.objects.all()
    hlinks = {}
    for link in header_links :
        if not link.page:
            hlinks['%s'%link.pos] = {
                'addr':link.addr, 
                'name':link.name
            }
        else:
            hlinks['%s'%link.pos] = {
                'addr':link.page.get_url(), 
                'name':link.page.title
            }
    flinks = FooterLink.objects.all()
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    services = ''
    selected_service = ''
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    set_as_dropship = False
    chosen_customer = ''

    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
        
    products = cart_object.get_items_in_cart()
    discount = 0
    discounted_price = 0
    shipping_origin = '' #ShippingOrigin.objects.filter(is_default = True)[0]
    if 'old_cart_weight' in request.session:
        if request.session['old_cart_weight'] != cart_object.get_total_weight():
            cart_object.shipping_cost = 0
            cart_object.save()
            request.session['old_cart_weight'] = cart_object.get_total_weight()
    else:
        request.session['old_cart_weight'] = cart_object.get_total_weight()

    if request.method == 'POST':
        method = request.POST.get('method', 'remove')
        item=""
        if method == 'check_shipping':
            costs_list = ''
            costs_list = get_cost(request.user, request.POST.get('courier', 'jne').lower())
            if costs_list:
                services = [x for x in costs_list]
                selected_service = request.POST['courier']
                cart_object.shipping_service = selected_service
                cart_object.save()
                request.session['services'] = services
                
            return JsonResponse(list(services), safe=False)
        elif method == 'set_shipping':
            if 'services' in request.session :
                services= request.session['services']
            user_selected_service = request.POST.get('service')
            for s in services:
                if s['service'] == user_selected_service :
                    cart_object.shipping_sub_service = user_selected_service
                    cart_object.shipping_cost = s['cost'][0]['int_value']
                    cart_object.save()
                    break
        elif method == 'add_dropship_address':
            form = CustomerAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                try:
                    customer = Customer()
                    customer.name = data.get('name')
                    customer.home_provinsi = data.get('provinsi_home').name
                    customer.kota_provinsi = Kota.objects.get(pk=request.POST.get('kota_home')).name
                    customer.home_kecamatan = Kecamatan.objects.get(pk=request.POST.get('kecamatan_home')).name
                    customer.home_kelurahan = Kelurahan.objects.get(pk=request.POST.get('kelurahan_home')).name
                    customer.home_address = data.get('home_address')
                    customer.seller = request.user.member
                    customer.save()
                    cart_object.is_set_as_dropship = True
                    cart_object.customer = customer
                    cart_object.shipping_address = customer.get_home_address()
                    shipping_cost = cart_object.shipping_cost = 0
                    cart_object.save()
                except:
                    pass

        elif method == 'cancel_dropship':
            cart_object.is_set_as_dropship = False
            cart_object.customer = None
            cart_object.shipping_address = ''
            shipping_cost = cart_object.shipping_cost = 0
            cart_object.save()

        elif method == 'set_dropship_address':
            try:
                customer = Customer.objects.get(id=request.POST.get('customer'))
                if customer:
                    cart_object.is_set_as_dropship = True
                    cart_object.customer = customer
                    cart_object.shipping_address = customer.get_home_address()
                    shipping_cost = cart_object.shipping_cost = 0
                    cart_object.save()
            except:
                pass
                    
        if cart_object.shipping_cost != 0 and cart_object.get_total_items_in_cart() == 0:
            shipping_cost = 0
        else:
            shipping_cost = cart_object.shipping_cost
            
    elif request.method == 'GET':
        if cart_object.shipping_cost != 0 and cart_object.get_total_items_in_cart() == 0:
            cart_object.shipping_cost = 231
            cart_object.save()
            
        shipping_cost = cart_object.shipping_cost
        
    if request.user.is_authenticated:
        discounted_price = cart_object.get_total_price()
        # if not request.user.member.member_type == Member.GUEST and \
        #     not request.user.member.member_type == Member.NEW_MEMBER:
        #     benefit = request.user.member.get_level()['BENEFIT']
        #     discount = cart_object.get_total_price() * discount / 100
        #     discounted_price = cart_object.get_total_price() * (100 - discount) / 100
        #     if discount <= 0:
        #         discount = int(discount)
        #         discounted_price = int(discounted_price)

    if shipping_cost:                
        discounted_price += shipping_cost

    couriers = get_courier()
    token = get_token(request)

    # customers = Customer.objects.filter(seller=request.user.member)
    # form = CustomerAddForm()
    return render(request, 'kei_store/order.html', 
        {'wishlist': wishlist_object,
        # 'customers':customers,
        'cart':cart_object,
        'products':products,
        'discount':discount,
        'hlinks':hlinks,
        'flinks':flinks, 
        'discounted_price':discounted_price,
        'couriers':couriers,
        'shipping_cost':shipping_cost,
        'services':services,
        'shipping_origin':shipping_origin,
        'selected_service':selected_service,
        'token':token,
        # 'form':form
        })

@login_required
def checkout(request):
    if not request.user.member.is_email_verified:
        return HttpResponseRedirect(reverse('membership:verify'))
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
    products = cart_object.get_items_in_cart()

    discount = 0
    discounted_price = 0

    if request.user.is_authenticated:
        discounted_price = cart_object.get_total_price()
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            benefit = request.user.member.get_level()['BENEFIT']
            discount = cart_object.get_total_price() * discount / 100
            discounted_price = cart_object.get_total_price() * (100 - discount) / 100
            if discount <= 0:
                discount = int(discount)
                discounted_price = int(discounted_price)
      
    order = PurchaseOrder.objects.get_or_create(user=request.user, is_paid=False, is_checked_out=False)[0]

    for item in products:
        order_item = PurchaseOrderItem.objects.get_or_create(purchase_order = order, product=item.product)[0]
        order_item.quantity = item.quantity
        order_item.product_referal = item.product_referal
        order_item.save()

    order.total_price = discounted_price
    order.discount = discount
    order.shipping_cost = cart_object.shipping_cost
    order.total_payment = discounted_price + cart_object.shipping_cost
    if not cart_object.shipping_address and not cart_object.is_set_as_dropship:
        order.alamat_tujuan = request.user.member.get_home_address()
    else:
        order.is_set_as_dropship = cart_object.is_set_as_dropship
        order.customer = cart_object.customer
        order.alamat_tujuan = cart_object.shipping_address
    order.service = cart_object.shipping_service.upper()
    order.sub_service = cart_object.shipping_sub_service
    order.save()
    order_detail = {key: format_order(key, value) for (key, value) in model_to_dict(order, 
            fields=["order_number",
                    "total_price", 
                    "total_payment", 
                    "shipping_cost", 
                    "alamat_tujuan",
                    "service",
                    "sub_service",
                    "discount"]).items()}
    return JsonResponse(order_detail, safe=False)

@login_required
def pay(request):
    if not request.user.member.is_email_verified:
        return HttpResponseRedirect(reverse('membership:verify'))
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
    cart_object.delete()
    order = PurchaseOrder.objects.filter(user=request.user, is_paid=False, is_checked_out = False)[0]
    order.is_checked_out = True
    order.is_paid = False
    order.is_verified = False
    order.payment_date = datetime.datetime.now()
    order.save()
    if request.user.is_authenticated:
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
                count_point(request,order)
                check_purchasing_bonus(request)
    del request.session['shopping_cart']
    cart = carts.get_cart(request)
    return HttpResponseRedirect(reverse('order:history'))


@login_required
def history(request):
    if not request.user.member.is_email_verified:
        return HttpResponseRedirect(reverse('membership:verify'))
    header_links = HeaderLink.objects.all()
    hlinks = {}
    for link in header_links :
        if not link.page:
            hlinks['%s'%link.pos] = {
                'addr':link.addr, 
                'name':link.name
            }
        else:
            hlinks['%s'%link.pos] = {
                'addr':link.page.get_url(), 
                'name':link.page.title
            }
    flinks = FooterLink.objects.all()
    orders = PurchaseOrder.objects.filter(user=request.user).order_by('-created_date')
    """
    if not orders:
        return HttpResponseRedirect(reverse('cart:index'))
    """
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    paginator = Paginator(orders,5)
    page = request.GET.get('page', 1)
    max_page = 4
    min_page = 0
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    max_page = products.number + 4
    min_page = products.number - 4
    token = get_token(request)
    return render(request, 'purchase_order/order_history.html', 
        {'wishlist': wishlist_object,
        'cart':cart_object,
        'token':token,
        'hlinks':hlinks,
        'flinks':flinks, 
        'products':products,
        'max_page':max_page,
        'min_page':min_page})

@login_required
def detail(request, order_number):
    if not request.user.member.is_email_verified:
        return HttpResponseRedirect(reverse('membership:verify'))
    header_links = HeaderLink.objects.all()
    hlinks = {}
    for link in header_links :
        if not link.page:
            hlinks['%s'%link.pos] = {
                'addr':link.addr, 
                'name':link.name
            }
        else:
            hlinks['%s'%link.pos] = {
                'addr':link.page.get_url(), 
                'name':link.page.title
            }
    flinks = FooterLink.objects.all()
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    order = PurchaseOrder.objects.get(order_number=order_number.upper())
    products = order.item_in_order.all()

    token = get_token(request)
    return render(request, 'purchase_order/order_detail.html', 
        {'wishlist': wishlist_object,
        'products': products,
        'cart':cart_object,
        'hlinks':hlinks,
        'flinks':flinks, 
        'token':token,
        'order':order})

def format_order(key, value):
    for x in ["order_number", "alamat_tujuan", "service", "sub_service"]:
        if key == x :
            return value
    return(int_to_rupiah(value))