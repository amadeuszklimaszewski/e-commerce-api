from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from src.apps.accounts.models import UserProfile
from src.apps.accounts.serializers import (
    UserAddressOutputSerializer,
    UserOrderOutputSerializer,
)
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


class OrderInputSerializer(serializers.Serializer):
    coupon_code = serializers.CharField()
    address_id = serializers.IntegerField(validators=[MinValueValidator(1)])


class OrderItemOutputSerializer(serializers.ModelSerializer):
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


class OrderOutputSerializer(serializers.ModelSerializer):
    userprofile = UserOrderOutputSerializer(
        source="user.userprofile", many=False, read_only=True
    )
    coupon = serializers.CharField(source="coupon.code")
    address = UserAddressOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "userprofile",
            "address",
            "coupon",
            "before_coupon",
            "total",
            "address",
            "payment_accepted",
            "order_accepted",
            "being_delivered",
            "received",
            "created",
            "updated",
        )
        read_only_fields = fields
