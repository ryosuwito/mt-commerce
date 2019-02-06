"""kei_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import membership.urls as membership
import database_wilayah.urls as wilayah
import storefront.urls as storefront
import shopping_cart.urls as cart
import purchase_order.urls as order
import shipping_backend.urls as shipping
from shipping_backend.views import shipping_redirect
from purchase_order.views import checkout, pay, history
from storefront.views import home
from blog_page.views import blog_index, page, article

urlpatterns = [
    path('admin/shipping_backend/shippingorigin/add/', RedirectView.as_view(url='/shipping/origin/', permanent=False)),
    path('admin/shipping_backend/shippingorigin/<int:pk>/change/', shipping_redirect),
    path('blog/<str:article_slug>/', article, name="blog_detail"),
    path('page/<str:page_slug>/', page, name="page_detail"),
    path('member/', include(membership, namespace='member_backend')),
    # path('guest/', include(membership, namespace='guest_backend')),
    path('wilayah/', include(wilayah, namespace='wilayah_backend')),
    path('cart/', include(cart, namespace='cart_backend')),
    path('checkout/', checkout, name="checkout"),
    path('pay/', pay, name="pay"),
    path('history/', history, name="history"),
    path('order/', include(order, namespace='order_backend')),
    path('shipping/', include(shipping, namespace='shipping_backend')),
    path('admin/', admin.site.urls),
    re_path(r'^$', home, name="home"),
    re_path(r'^blog/$', blog_index, name="blog_index"),
    re_path(r'^store/', include(storefront, namespace='store_backend')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)