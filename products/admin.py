from django.contrib import admin
from .models import ProductsCategory, Products, Order, Favorite,Comment,Logo, DeliveryLocations, OrderProduct
# Register your models here.
admin.site.register(ProductsCategory)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Logo)
admin.site.register(DeliveryLocations)
admin.site.register(OrderProduct)