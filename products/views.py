from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import ProductsCategory, Products, Order, Favorite, Comment, Logo, OrderProduct
from .forms import CommentForm, OrderProductForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone


# Create your views here.


class ProductsCategoryView(View):
    def get(self, request):
        products_category = ProductsCategory.objects.all()
        logo = Logo.objects.first()
        context = {
            'products_category': products_category,
            'logo': logo
        }
        return render(request, 'products_category.html', context=context)


class ProductsAllView(View):
    def get(self, request):
        products = Products.objects.all()
        categories = ProductsCategory.objects.all()
        logo = Logo.objects.first()
        context = {
            'products': products,
            'categories': categories,
            'logo': logo
        }
        return render(request, 'home.html', context=context)


class ProductsView(View):
    def get(self, request, pk):
        items = Products.objects.filter(category=pk)
        logo = Logo.objects.first()
        context = {
            'items': items,
            'logo': logo
        }
        return render(request, 'products.html', context=context)


class ProductsDetailView(View):
    def get(self, request, pk):
        products = get_object_or_404(Products, pk=pk)
        comments = Comment.objects.filter(product_id=pk)
        form = CommentForm()
        logo = Logo.objects.first()
        result = [comment.star_given for comment in comments if 1 < comment.star_given < 6]
        average = round(sum(result) / len(result), 1) if result else None
        category_products = Products.objects.filter(category=products.category).exclude(pk=products.id)
        context = {
            'products': products,
            'result': result,
            'average': average,
            'comment_detail': comments,
            'category_products': category_products,
            'form': form,
            'logo': logo
        }
        return render(request, 'products_detail.html', context=context)


class AddCommentView(View):
    def post(self, request, pk):
        products = get_object_or_404(Products, pk=pk)
        form = CommentForm(request.POST)
        logo = Logo.objects.first()
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
            'form': form,
            'logo': logo
        }
        return render(request, 'products_detail.html', context=context)


class UpdateCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        update_comment_form = CommentForm(instance=comment)
        return render(request, 'update_comment.html',
                      context={'update_comment_form': update_comment_form, 'comment': comment})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        update_comment_form = CommentForm(request.POST, instance=comment)
        if update_comment_form.is_valid():
            update_comment_form.save()
            return redirect('products:products_detail', pk=comment.product.pk)  # Redirect to the product detail page
        return render(request, 'update_comment.html',
                      context={'update_comment_form': update_comment_form, 'comment': comment})


class DeleteCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        product = comment.product  # Assuming comment has a foreign key to product
        comment.delete()

        return redirect(reverse('products:products_detail', kwargs={'pk': product.pk}))


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


class LogoView(View):
    def get(self, request):
        logo = Logo.objects.first()

        context = {'logo': logo}
        return render(request, 'base.html', context=context)


class AddToOrderView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        order, created = Order.objects.get_or_create(
            user=request.user,
            product_name=product,
            defaults={'quantity': 1}
        )

        if not created:
            order.quantity += 1
            order.save()

        return redirect('products:cart_detail')


class DeleteFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        order = get_object_or_404(Order, user=request.user, product_name=product)
        order.delete()

        return redirect('products:cart_detail')


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        logo = Logo.objects.first()
        context = {
            'orders' : orders,
            'logo' : logo
        }
        return render(request, 'cart_detail.html', context=context)


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        order = get_object_or_404(Order, user=request.user, product_name=product)

        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > 0:
            order.quantity = new_quantity
            order.save()
        else:
            order.delete()

        return redirect('products:cart_detail')


class AddToFavoriteView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        Favorite.objects.get_or_create(user=request.user, product=product)
        messages.add_message(request, messages.SUCCESS, 'Added to Favorites')
        return redirect('products:products_detail', pk=product_id)


class RemoveFromFavoriteView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        favorite = Favorite.objects.filter(user=request.user, product=product)
        if favorite.exists():
            favorite.delete()
        return redirect('products:favorite_list')


class FavoriteListView(LoginRequiredMixin, View):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        logo = Logo.objects.first()
        context = {
            'favorites': favorites,
            'logo' : logo
        }
        return render(request, 'favorite_list.html', context=context)


class OrderProductsView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        order_card_form = OrderProductForm()
        logo = Logo.objects.first()
        return render(request, 'order_product.html', {'order_card_form': order_card_form, 'product': product, 'logo':logo})

    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        order_card_form = OrderProductForm(request.POST or None)
        if request.method == 'POST':
            if order_card_form.is_valid():
                order_product = order_card_form.save(commit=False)
                order_product.user = request.user
                order_product.product = product
                order_product.ordered_time = timezone.now()
                order_product.save()
                return redirect('products:view_orders')
        return render(request, 'order_product.html', {'order_card_form': order_card_form, 'product': product})


class OrdersView(View):
    def get(self, request):
        orders = OrderProduct.objects.filter(user=request.user)
        logo = Logo.objects.first()
        context = {
            'orders': orders,
            'logo' : logo
        }
        return render(request, 'view_orders.html', context=context)


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        order_product = get_object_or_404(OrderProduct, id=product_id, user=request.user)
        order_product.delete()
        return redirect('products:view_orders')
