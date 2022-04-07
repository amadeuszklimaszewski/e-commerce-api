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
from src.apps.orders.validators import validate_item_quantity
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
        product_instance = get_object_or_404(Product, id=product_id)
        max_quantity = product_instance.inventory.quantity
        validate_item_quantity(quantity, max_quantity)
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
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

    @classmethod
    def _check_quantity(cls, instance: CartItem, quantity: int):
        if quantity == 0:
            instance.delete()
            return False
        return True

    @classmethod
    @transaction.atomic
    def update_cart_item(cls, instance: CartItem, validated_data: dict):
        quantity = validated_data["quantity"]
        max_quantity = instance.product.inventory.quantity
        validate_item_quantity(quantity, max_quantity)
        if cls._check_quantity(instance, quantity):
            try:
                setattr(instance, "quantity", quantity)
            except KeyError as err:
                raise err(f"{err} : Missing or wrong data")
            instance.save()
            return instance
        return
