from apps.users.models import User
from django.db import models

# Create your models here.
from apps.catalog.models import Product, ProductOption


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    ACTIVE, SAVED_FOR_LATER, DELETED = 1, 2, 0
    status_choices = ((ACTIVE, 'Active'), (SAVED_FOR_LATER, 'Saved for Later'), (DELETED, 'Deleted'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_price = models.FloatField()
    discount = models.FloatField(default=0.0)
    discounted_price = models.FloatField()
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status = models.IntegerField(default=ACTIVE, choices=status_choices)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)



