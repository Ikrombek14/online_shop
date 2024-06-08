from django.shortcuts import redirect, render, get_object_or_404
from .models import ProductsCategory, Products, Order, Favorite, Comment
from .forms import CommentForm
from django.views import View
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q

# Create your views here.


        
class ProductsCategoryView(View):
    def get(self, request):
        products_category = ProductsCategory.objects.all()
        context = {
            'products_category': products_category
        }
        return render(request, 'products_category.html', context=context)

class ProductsAllView(View):
    def get(self,request):
        products = Products.objects.all()
        categories = ProductsCategory.objects.all()
        context = {
            'products' : products,
            'categories' : categories
        }
        return render(request, 'home.html', context=context)


class ProductsView(View):
    def get(self, request, pk):
        items = Products.objects.filter(category=pk)
        context = {
            'items' : items
        }
        return render(request, 'products.html', context=context)


class ProductsDetailView(View):
    def get(self, request, pk):
        products = get_object_or_404(Products, pk=pk)
        comments = Comment.objects.filter(product_id=pk)
        form = CommentForm()
        result = [comment.star_given for comment in comments if 1 < comment.star_given < 6]
        average = round(sum(result) / len(result), 1) if result else None
        category_products = Products.objects.filter(category=products.category).exclude(pk=products.id)
        context = {
            'products': products,
            'result': result,
            'average': average,
            'comment_detail': comments,
            'category_products': category_products,
            'form': form
        }
        return render(request, 'products_detail.html', context=context)

class AddCommentView(View):
    def post(self, request, pk):
        products = get_object_or_404(Products, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = products
            comment.save()
            return redirect('products:products_detail', pk=pk)  # Redirect to product detail view after saving

        # If form is not valid, re-render the detail page with form errors
        comments = Comment.objects.filter(product_id=pk)
        result = [comment.star_given for comment in comments if 1 < comment.star_given < 6]
        average = round(sum(result) / len(result), 1) if result else None
        category_products = Products.objects.filter(category=products.category).exclude(pk=products.id)
        context = {
            'products': products,
            'result': result,
            'average': average,
            'comment_detail': comments,
            'category_products': category_products,
            'form': form
        }
        return render(request, 'products_detail.html', context=context)

class UpdateCommentView(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return render(request, 'products_detail.html', context={'form': form})

class DeleteCommentView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return render(request, 'products_detail.html', context={'form': CommentForm()})


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        items = Products.objects.filter(
            Q(Q(name__icontains=query) | Q(price__icontains=query) | Q(description__icontains=query))
        )
        context = {
            'items': items,
            'query': query
        }
        return render(request, 'search.html', context=context)
