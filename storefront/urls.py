from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'storefront'
 
urlpatterns = [
	path('create/', views.create_new_store, name='create_new_store'),
	path('add/', views.add_new_product, name='add_new_product'),
    path('detail/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('kategori/<int:category_pk>/', views.product_by_category, name='product_by_category'),
    path('price/<int:start_price>/<int:end_price>/', views.product_by_price, name='product_by_price'),
    re_path(r'kategori/$', RedirectView.as_view(url='/store/')),
    re_path(r'detail/$', RedirectView.as_view(url='/store/')),
    re_path(r'price/$', RedirectView.as_view(url='/store/')),
    path('<str:store_slug>/', views.product_by_store, name='products_in_store'),
    re_path(r'^$', views.index, name='product_all'),
]
