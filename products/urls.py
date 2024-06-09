from django.urls import path
from .views import (ProductsCategoryView, ProductsView,
                    ProductsDetailView, AddCommentView, DeleteCommentView,
                    UpdateCommentView, SearchView, ProductsAllView, LogoView)

app_name = 'products'
urlpatterns = [
    path('categories/', ProductsCategoryView.as_view(), name='categories'),
    path('', ProductsAllView.as_view(), name='products'),
    path('products/<int:pk>/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/detail/', ProductsDetailView.as_view(), name='products_detail'),
    path('products/<int:pk>/add-comment/', AddCommentView.as_view(), name='add_comment'),
    path('update-comment/<int:pk>/', UpdateCommentView.as_view(), name='update_comment'),
    path('delete-comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('', LogoView.as_view(), name='logo')
    ]