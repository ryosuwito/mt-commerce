from django.urls import path, re_path
from django.views.generic import RedirectView 
from . import views

app_name = 'storefront'
 
urlpatterns = [
	path('create/', views.create_new_store, name='create_new_store'),
	path('add/', views.add_new_product, name='add_new_product'),
    path('<str:store_slug>/', views.product_by_store, name='products_in_store'),
    re_path(r'^$', views.index, name='product_all'),
]
