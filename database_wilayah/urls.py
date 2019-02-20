from django.urls import path
from . import views

app_name = 'wilayah'

urlpatterns = [
    path('kota/<str:nama_provinsi>/', views.get_kota, name='kota'),
    path('kecamatan/<int:pk>/', views.get_kecamatan, name='kecamatan'),
    path('kelurahan/<int:pk>/', views.get_kelurahan, name='kelurahan'),
]                       