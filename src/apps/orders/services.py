from email.headerregistry import Address
from ipaddress import collapse_addresses
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from src.apps.orders.models import (
    Order,
    OrderItem,
    Cart,
    CartItem,
    Coupon,
)
from src.apps.products.models import Product

User = get_user_model()


class CouponService:
    """
    Service for creating and updating coupons.
    """

    @classmethod
    @transaction.atomic
    def update_coupon(cls, instance: Coupon, validated_data: dict) -> Coupon:
        fields = [
            "code",
            "amount",
            "is_active",
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except (Error := KeyError):
                raise Error(f"{Error} : Missing data")
        instance.save()
        return instance


class CartService:
    @classmethod
    @transaction.atomic
    def create_cart_item(cls, cart_id: int, validated_data: dict) -> CartItem:
        product_id = validated_data.pop("product_id")
        quantity = validated_data.pop("quantity")
        try:
            cartitem = CartItem.objects.get(product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
        except CartItem.DoesNotExist:
            product_instance = get_object_or_404(Product, id=product_id)
            cart_instance = get_object_or_404(Cart, id=cart_id)
            cartitem = CartItem.objects.create(
                cart=cart_instance,
                product=product_instance,
                quantity=quantity,
            )
            cartitem.save()
        return cartitem
