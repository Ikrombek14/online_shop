from django.forms import ModelForm, forms
from .models import ProductsCategory, Products, Order, Favorite, Comment, CustomUser, OrderProduct


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'star_given']


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['user_email', 'delivery_location', 'phone_number']
