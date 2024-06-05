from django.shortcuts import render
from .models import ProductsCategory, Products, Order, Favorite, Comment
from django.views import View
# Create your views here.
class ProductsCategoryView(View):
    def get(self,request):
        products_category = ProductsCategory.objects.all()
        context = {
            'products_category': products_category
        }
        return render(request, 'Products/products_category.html', context=context)


class ProductsView(View):
    def get(self, request, pk):
        items = Products.objects.get(category=pk)
        context = {
            'items' : items
        }
        return render(request, 'Products/products.html', context=context)


class ProductsDetailView(View):
    def get(self, request, pk):
        products = Products.objects.get(pk=pk)
        comments = Comment.objects.filter(product_id=pk)
        result = [comment.star_given for comment in comments if 1 < comment.star_given < 6]
        average = round(sum(result) / len(result), 1) if result else None
        context = {
            'products' : products,
            'result' : result,
            'average' : average
        }
        return render(request, 'Products/products_detail.html', context=context)

