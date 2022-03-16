import logging

from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import CartItemSerializer, AttachCartItemSerializer
from apps.catalog.models import ProductOption, Product
from apps.common.responses import APIResponse

logger = logging.getLogger(__name__)


class CartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permissions = [IsAuthenticated]

    def get_or_create_cart(self, user):
        cart = Cart.objects.filter(user=user).last()
        if not cart:
            cart = Cart.objects.create(user=user)
        return cart

    def list(self, request, *args, **kwargs):
        cart = self.get_or_create_cart(request.user)
        cart_items = CartItem.objects.select_related(
            'product', 'product_option'
        ) .filter(cart=cart, status=CartItem.ACTIVE)
        results = {
            "cart_id": cart.id,
            "cart_items": CartItemSerializer(cart_items, many=True).data
        }
        return APIResponse(
            status='SUCCESS', code=200,
            message='Cart Generated successfully', extra_fields={"results": results}
        ).json

    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def attach(self, request):
        serializer = AttachCartItemSerializer(request.data)
        if not serializer.is_valid():
            return APIResponse(
                status='FAILED', code=400,
                message='Invalid Details', errors=serializer.errors
            ).json

        data = serializer.data
        cart = self.get_or_create_cart(request.user)
        product = Product.objects.filter(id=data.get("product_id")).last()
        product_option = ProductOption.objects.filter(id=data.get("product_option_id")).last()
        if not product or not product_option:
            raise Exception('Invalid Details for Product/ProductOption')
        cart_item = CartItem.objects.filter(
            cart=cart, product=product, product_option_id=product_option, status=CartItem.ACTIVE
        ).last()
        if not cart_item:
            cart_item = CartItem()
            cart_item.product = product
            cart_item.product_option_id = product_option
        cart_item.quantity = data.get("quantity")
        if cart_item.quantity == 0:
            cart_item.status = CartItem.DELETED
        cart_item.cart = cart
        cart_item.product_price = cart.product_option.price
        cart_item.save()
        return APIResponse(
            status='SUCCESS', code=200,
            message='Product added to Cart Successfully'
        ).json

    @action(detail=False, methods=["DELETE"])
    @transaction.atomic
    def clear(self, request):
        cart = self.get_or_create_cart(request.user)
        CartItem.objects.filter(cart=cart).update(status=CartItem.DELETED)
        return APIResponse(
            status='SUCCESS', code=200,
            message='Products removed from Cart Successfully'
        ).json
