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
