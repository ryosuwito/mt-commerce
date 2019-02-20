from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path('wishlist/', views.wishlist_index, name='wishlist_index'),
    re_path(r'$', views.index, name='index'),
]