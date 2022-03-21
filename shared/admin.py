from django.contrib import admin
from .models import Isdist
from manuf.models import Products
from dist.models import QRUp
# Register your models here.
admin.site.register(Products)
admin.site.register(Isdist)
admin.site.register(QRUp)
