
from django.urls import path, re_path
from . import views

app_name = 'order'

urlpatterns = [
    path('detail/<str:order_number>/', views.detail, name='detail'),
    path('checkout/', views.checkout, name='chekout'),
    path('history/', views.history, name='history'),
    re_path(r'$', views.index, name='prepare'),
]