from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    sku_code = models.CharField(max_length=50, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class ProductOption(models.Model):
    choices = ((1, 'Available'), (2, 'Out Stock'), (3, 'Up Coming'))
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=choices, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class ProductAttributes(models.Model):
    product_option = models.ForeignKey(ProductOption, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class ProductImages(models.Model):
    mode = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    product_option = models.ForeignKey(ProductOption, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)