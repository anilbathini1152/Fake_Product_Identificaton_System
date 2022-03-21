from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home',views.manuhome,name='manuhome'),
    path('addp',views.addprod,name='addp'),
    path('mprof', views.mprof, name = 'mprof'),
    path('profimgup', views.profimgup, name = 'profimgup'),
]