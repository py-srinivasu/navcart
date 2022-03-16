import logging

from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import Cart, CartItem

from apps.common.responses import APIResponse
from apps.order.models import Order

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permissions = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).last()
        cart_items = CartItem.objects.filter(cart=cart)
        # TODO: Need to add logic for Creating Order Object


    def list(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        # TODO: Need to create Order Serializer
        order_serializer = OrderSerializer(orders, many=True)
        return APIResponse(
            status='SUCCESS', code=200,
            message='Orders List Generated successfully', extra_fields={"results": order_serializer.data}
        ).json

    @action(detail=False, methods=["DELETE"])
    @transaction.atomic
    def cancel(self, request, pk):
        pass
