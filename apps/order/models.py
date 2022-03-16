from apps.users.models import User
from django.db import models

# Create your models here.
from apps.cart.models import Cart
from apps.catalog.models import Product, ProductOption


class Order(models.Model):
    status_choices = ((1, 'Pending'), (2, 'In Transit'), (3, 'Delivered'),
                      (0, 'Cancelled'), (4, 'Refund Initiated'), (5, 'Refund Processed'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    payment_mode = models.CharField(max_length=50, default='COD')
    order_total = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    total_products = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=status_choices)


class OrderItem(models.Model):
    status_choices = ((1, 'Pending'), (2, 'In Transit'), (3, 'Delivered'),
                      (0, 'Cancelled'), (4, 'Refund Initiated'), (5, 'Refund Processed'))
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product_price = models.FloatField()
    discount = models.FloatField(default=0.0)
    discounted_price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=status_choices)