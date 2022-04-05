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
