from rest_framework import serializers


def validate_item_quantity(quantity, max_quantity):
    if quantity > max_quantity:
        raise serializers.ValidationError(
            {"quantity": "not enough available products in stock"},
        )


def validate_coupon_total(total, min_total):
    if total < min_total:
        raise serializers.ValidationError(
            {"coupon": "Order total is too low to use this coupon."}
        )
