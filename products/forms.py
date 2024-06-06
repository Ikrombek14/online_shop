from django.forms import ModelForm
from .models import ProductsCategory, Products, Order, Favorite, Comment,CustomUser


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'star_given']

