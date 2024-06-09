from django.contrib import admin
from .models import ProductsCategory, Products, Order, Favorite,Comment,Logo
# Register your models here.
admin.site.register(ProductsCategory)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Logo)