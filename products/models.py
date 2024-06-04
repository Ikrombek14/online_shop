from django.db import models
# Create your models here.

class ProductsCategory(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'products_category'

    def __str__(self):
        return self.name


class ProductsMake(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'products_make'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(ProductsCategory, on_delete=models.DO_NOTHING)
    characteristics = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    make = models.ForeignKey(ProductsMake, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='products_images/', blank=True, null=True, default='not_available.png')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f'{self.name} - {self.category.name}'