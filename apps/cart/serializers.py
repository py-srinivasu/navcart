from apps.cart.models import CartItem
from rest_framework import serializers

from apps.catalog.serializers import ProductSerializer, ProductOptionSerializer


class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    # product_option = ProductOptionSerializer(many=True)

    class Meta:
        fields = ['id', 'product', 'product_option', 'product_price', 'discount', 'discounted_price', 'modified_on']
        model = CartItem
        depth = 1


class AttachCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_option_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class RemoveCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_option_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
