from django.db import models
from users.models import CustomUser


# Create your models here.

class ProductsCategory(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'products_category'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(ProductsCategory, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='products_images/', blank=True, null=True, default='not_available.png')
    description = models.TextField()
    price = models.IntegerField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    product_name = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"Order ID: {self.pk} | User: {self.user.username} | Product: {self.product.name} | Price: {self.product.price} | Date: {self.order_date}"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        unique_together = ('user', 'product')  # Ensure a product can only be favorited once per user

    def __str__(self):
        return f"User: {self.user.username} | Product: {self.product.name}"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    star_given=models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"User: {self.user.username} | Product: {self.product.name} | Comment: {self.comment} | Star Given: {self.star_given} | Date: {self.date}"