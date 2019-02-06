from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'membership'

urlpatterns = [
    path('profile/<str:uname>/', views.profile_page, name='profile'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    # path('register/<str:referal_code>/', views.register_page, name='register'),
    path('register/', views.register_page, name='register'),
    # path('choose/<str:referal_code>/', views.pre_register_page, name='pre_register'),
    # path('choose/', views.pre_register_page, name='pre_register'),
    path('profile/edit', views.edit_profile_page, name='edit_profile'),
    path('profile/', views.profile_page, name='profile'),
    path('verification/es/', views.verified_es, name='email_verify_success'),
    path('verification/ps/', views.verified_ps, name='phone_verify_success'),
    path('verification/ff/', views.verified_ff, name='verification_fail'),
    path('verify/resend/', views.verify_resend, name='verify_email_resend'),
    path('verify/<str:vericode>/', views.verify, name='verify_email'),
    path('phone-verify/<str:phonecode>/', views.verify, name='verify_phone'),
    re_path(r'verify/$', views.verify, name='verify'),
    re_path(r'phone-verify/$', RedirectView.as_view(url='/member/verify/')),
]