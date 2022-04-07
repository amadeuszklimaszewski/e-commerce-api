from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from src.apps.orders.models import (
    Order,
    OrderItem,
    Cart,
    CartItem,
    Coupon,
)


class CouponInputSerializer(serializers.Serializer):
    code = serializers.CharField()
    amount = serializers.IntegerField()
    is_active = serializers.BooleanField()


class CouponOutputSerializers(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "amount",
            "is_active",
            "created",
            "updated",
        )
        read_only_fields = fields


class CartItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, validators=[MinValueValidator(1)])


class CartItemQuantityInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, validators=[MinValueValidator(0)])


class CouponOrderInputSerializer(serializers.Serializer):
    code = serializers.CharField()


class CartItemOutputSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_id",
            "quantity",
            "total_item_price",
            "total_discount_item_price",
            "amount_saved",
            "final_price",
        )
        read_only_fields = fields


class CartOutputSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    cart_items = CartItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "username",
            "cart_items",
            "total",
        )
        read_only_fields = fields
