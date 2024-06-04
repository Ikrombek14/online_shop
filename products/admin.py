from django.contrib import admin
from .models import ProductsMake, ProductsCategory, Products
# Register your models here.

admin.site.register(Products)
admin.site.register(ProductsCategory)
admin.site.register(ProductsMake)