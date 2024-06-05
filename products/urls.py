from django.urls import path
from .views import ProductsCategoryView, ProductsView, ProductsDetailView

app_name = 'products'
urlpatterns = [
    path('categories/', ProductsCategoryView.as_view(), name='categories'),
    path('products/<int:pk>/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/detail/', ProductsDetailView.as_view(), name='products_detail'),

]