from django.forms import forms
from .models import ProductsCategory, Products, Order, Favorite, Comment,CustomUser


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'star_given']

