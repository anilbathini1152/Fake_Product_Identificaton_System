from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('verifyQR',views.qr_image_view,name='qr_image_view'),
    path('signup',views.usignup, name='usignup'),
    path('login',views.ulogin, name='login'),
    path('logout',views.ulogout, name='logout'),
    path('uprof',views.uprof, name='uprof'),
    path('profimgup', views.profimgup, name = 'profimgup'),
    
]