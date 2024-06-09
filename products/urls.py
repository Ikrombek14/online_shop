from django.urls import path
from .views import (ProductsCategoryView, ProductsView,
                    ProductsDetailView, AddCommentView, DeleteCommentView,
                    UpdateCommentView, SearchView, ProductsAllView, LogoView,
                    AddToOrderView, DeleteFromCartView, CartDetailView, UpdateCartItemView,
                    AddToFavoriteView, RemoveFromFavoriteView, FavoriteListView     )

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
    path('', LogoView.as_view(), name='logo'),
    path('add/<int:product_id>/order', AddToOrderView.as_view(), name='add_order'),
    path('delete/<int:product_id>/from_cart', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('cart/', CartDetailView.as_view(),  name='cart_detail'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('product/<int:product_id>/add_to_favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('product/<int:product_id>/remove_from_favorite/', RemoveFromFavoriteView.as_view(), name='remove_from_favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
]