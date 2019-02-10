from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from catalog.models import Product, Category, Store
from membership.models import Member
from shopping_cart.models import Cart, CartItem, WishList, WishListItem
from shopping_cart import carts, wishlists
from django.urls import reverse
from membership.views import check_host
from membership.templatetags.int_to_rupiah import int_to_rupiah
from settings.models import HeaderLink, HomeLink, FooterLink
from blog_page.models import Article
from membership.forms import MemberRegisterForm

import datetime
import random

from .forms import ProductCartForm, AddProductForm, CreateNewStoreForm

def home(request):
    header_links = HeaderLink.objects.all()
    articles = Article.objects.all().order_by('created_date')
    form = MemberRegisterForm()
    if len(articles) > 5:
        articles = articles[:5]
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
    try:
        products = Product.objects.filter(is_archived=False).order_by('-pk')[:4]
        featured_products = Product.objects.filter(is_featured=True).order_by('-pk')[0]
    except:
        products = {}
        featured_products = {}
    categories = Category.objects.all()
    stores = Store.objects.all()
    return render(request, 'kei_store/index.html', 
        {
        'form':form,
        'articles':articles,
        'hlinks':hlinks,
        'flinks':flinks,
        'cart':cart_object, 
        'stores':stores,
        'categories':categories,
        'products':products,
        'featured_products':featured_products})
    #push error

def product_detail(request, product_pk, **kwargs):
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
    referal_code = redirect_referal_code(request, kwargs=kwargs)
    if referal_code['code']:
        referer = Member.objects.get(referal_code = referal_code['code'])
    else:
        referer = ''

    if referal_code['message'] == "redirect_to_default":
        return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                reverse('storefront:product_detail', kwargs={'product_pk':product_pk},
                    current_app=request.resolver_match.namespace))
    elif referal_code['message'] == 'redirect_to_referal':
        return HttpResponseRedirect(request.scheme+"://"+referer.user.username+'.'+settings.DEFAULT_HOST + 
                reverse('storefront:product_detail', kwargs={'product_pk':product_pk},
                    current_app=request.resolver_match.namespace))

    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    categories = Category.objects.all()
    stores = Store.objects.all()
    all_product = Product.objects.filter(is_archived=False).exclude(pk=product_pk)
    is_wishlist = False
    if len(all_product) >= 5:
        other_product = random.sample(list(all_product), 4)
    else:
        other_product = random.sample(list(all_product), len(all_product))

    product = Product.objects.get(pk=product_pk)
    is_in_wishlist = False

    if request.method == 'POST':
        method = ''
        try:
            method = request.POST['method']
        except:
            pass
        
        if method == 'wishlist':  
            is_wishlist = True 
            wishlist_item = WishListItem.objects.get_or_create(wishlist=wishlist_object, product=product)[0]
       
        elif method == 'cart':
            form = ProductCartForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                quantity = data.get('quantity')
                cart_item = False
                try :
                    cart_item = CartItem.objects.get_or_create(cart=cart_object, product=product)[0]
                except:
                    pass

                if not cart_item.quantity :
                    cart_item.quantity = quantity
                else :
                    cart_item.quantity += int(quantity)

                if request.user.is_authenticated:
                    if referer and not referer == request.user.member:
                        cart_item.product_referal = referer
                else: 
                    if referer:
                        cart_item.product_referal = referer
                    
                cart_item.save()
            
            return HttpResponseRedirect(reverse('cart:index', 
                current_app=request.resolver_match.namespace))

    form = ProductCartForm()

    product = Product.objects.get(pk=product_pk)

    discount = 0
    discounted_price = product.price
    
    if request.user.is_authenticated:
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            discount = request.user.member.get_level()['BENEFIT']
            discounted_price = product.price * (100 - discount) / 100

    products_in_wishlist = [x.product.id for x in wishlist_object.item_in_wishlist.all()]
    for pk in products_in_wishlist:
        if product_pk == pk:
            is_in_wishlist = True

    if is_wishlist:
        response = HttpResponseRedirect(reverse("storefront:product_detail", kwargs=
            {'product_pk':product_pk})[:-1]+"#formQuantity")
    else:
        response = render(request, 'storefront/product_detail.html', 
            {
            'hlinks':hlinks,
            'flinks':flinks,
            'product':product, 
            'other_product':other_product, 
            'cart':cart_object, 
            'wishlist':wishlist_object, 
            'form':form, 
            'stores':stores,
            'categories':categories,
            'is_in_wishlist': is_in_wishlist,
            'discount': discount, 
            'discounted_price': int(discounted_price)})

    return response
    
def index(request, **kwargs):
    referal_code = redirect_referal_code(request, kwargs=kwargs)
    if referal_code['code']:
        referer = Member.objects.get(referal_code = referal_code['code'])

    if referal_code['message'] == "redirect_to_default":
        return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                reverse('storefront:product_all', 
                    current_app=request.resolver_match.namespace))
    elif referal_code['message'] == 'redirect_to_referal':
        return HttpResponseRedirect(request.scheme+"://"+referer.user.username+'.'+settings.DEFAULT_HOST + 
                reverse('storefront:product_all', 
                    current_app=request.resolver_match.namespace))


    try:
        product_list = Product.objects.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk'
    return paginate_results(request, product_list,product_title)
    
def product_by_category(request, category_pk, **kwargs):
    try:
        kategori = Category.objects.get(pk=category_pk)
        product_list = kategori.products_in_category.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk %s' % (kategori.name.title())
    return paginate_results(request, product_list,product_title)

def product_by_store(request, store_slug, **kwargs):
    try:
        store = Store.objects.get(slug=store_slug)
        product_list = store.products_in_store.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk %s' % (store.name.title())
    return paginate_results(request, product_list,product_title)

def product_by_price(request, start_price, end_price, **kwargs):
    try:
        if start_price < end_price and end_price > 0:
            product_list = Product.objects.filter(is_archived=False, 
                            price__range=(start_price, end_price)).order_by('price')
        else:
            product_list = Product.objects.filter(is_archived=False, 
                            price__gte=start_price).order_by('price')
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk dari %s - %s' % (int_to_rupiah(start_price), int_to_rupiah(end_price))
    return paginate_results(request, product_list,product_title)

def paginate_results(request, product_list,product_title):
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
    categories = Category.objects.all()
    stores = Store.objects.all()
    max_page = 4
    min_page = 0
    products = ''
    if product_list:
        try:
            paginator = Paginator(product_list,12)
            page = request.GET.get('page', 1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            max_page = products.number + 4
            min_page = products.number - 4
        except:
            pass

    response = render(request, 'kei_store/kategori.html', 
        {
         'hlinks':hlinks,
         'flinks':flinks,
         'cart':cart_object,
         'stores':stores,
         'categories':categories,
         'wishlist':wishlist_object, 
         'products':products,
         'categories':categories,
         'product_title':product_title,
         'max_page':max_page,
         'min_page':min_page})
    return response

@login_required(login_url='/member/login')
def add_new_product(request):
    try:
        store = request.user.store
    except:    
        store = ''
    if not store:
        return HttpResponseRedirect(reverse('storefront:create_new_store'))
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
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            product_name = data.get('name')
            product_price = data.get('price')
            product_weight = data.get('unit_weight')
            product_brand = data.get('brand')
            product_description = data.get('description')
            product_photo = data.get('photo')
            product_photo_alt1 = data.get('photo_alt1')
            product_photo_alt2 = data.get('photo_alt2')

            product = Product.objects.create(
                store = store,
                name = product_name,
                price = product_price,
                unit_weight = product_weight,
                description = product_description,
                photo = product_photo,
                photo_alt1 = product_photo_alt1,
                photo_alt2 = product_photo_alt2
                )

            if product:
                return HttpResponseRedirect(reverse('membership:profile'))

    elif request.method == 'GET': 
        form = AddProductForm()

    return render(request, 'kei_store/tambah_produk.html', 
        {'form': form, 
         'hlinks':hlinks,
         'flinks':flinks, 
         'wishlist': wishlist_object,
         'cart': cart_object,
        })

@login_required(login_url='/member/login')
def create_new_store(request):
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
    if request.method == 'POST':
        form = CreateNewStoreForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            store_name = data.get('name')
            store_description = data.get('description')
            store_photo = data.get('photo')

            store = Store.objects.create(
                owner=request.user,
                name=store_name,
                description=store_description,
                photo=store_photo
                )
            if store:
                return HttpResponseRedirect(reverse('storefront:add_new_product'))
    elif request.method == 'GET': 
        form = CreateNewStoreForm()

    return render(request, 'kei_store/buka_toko.html', 
        {'form': form, 
         'hlinks':hlinks,
         'flinks':flinks, 
         'wishlist': wishlist_object,
         'cart': cart_object,
        })