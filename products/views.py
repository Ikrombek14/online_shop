from django.shortcuts import render
from .models import ProductsCategory, Products, Order, Favorite,Comment
# Create your views here.
class ProductsCategoryView(View):
    def get(self,request):
        products_category = ProductsCategory.objects.all()
        context = {
            'products_category': products_category
        }
        return render(request, 'products_category.html', context=context)