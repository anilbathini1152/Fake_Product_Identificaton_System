from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home',views.disthome,name='disthome'),
    path('verifyQR', views.qr_image_view, name = 'image_upload'),
    path('verifyproduct', views.verify_prod, name = 'verify_prod'),
    path('dprof', views.dprof, name = 'dprof'),
    path('profimgup', views.profimgup, name = 'profimgup'),
]