from django.urls import path, re_path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('<int:pk>/change/', views.ChangeShippingOrigin.as_view(), name="change_origin"),
    path('<int:pk>/default/', views.set_default, name="set_default"),
    path('origin/', views.SetShippingOrigin.as_view(), name="origin"),
    path('province/id', views.get_province_id, name='get_province_id'),
    path('province/', views.get_province, name='get_province'),
    path('city/id', views.get_city_id, name='get_city_id'),
    path('city/', views.get_city, name='get_city'),
    path('cost/', views.get_cost, name='get_cost'),
]