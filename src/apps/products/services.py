from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from src.apps.products.models import (
    ProductCategory,
    ProductInventory,
    Product,
    ProductReview,
)


User = get_user_model()


class ProductService:
    """
    Service used to handle creation and update of product instances.
    """

    @classmethod
    @transaction.atomic
    def create_product(cls, validated_data: dict) -> Product:
        inventory_data = validated_data.pop("inventory")
        category_data = validated_data.pop("category")
        discount_data = validated_data.pop("discount")

        inventory = ProductInventory.objects.create(**inventory_data)
        category, created = ProductCategory.objects.get_or_create(**category_data)

        product = Product.objects.create(
            inventory=inventory, category=category, **validated_data
        )
        if discount_data:
            if percentage := discount_data.get("percentage", None):
                product.set_discount(percentage)
        return product

    @classmethod
    @transaction.atomic
    def update_product(cls, instance: Product, validated_data: dict) -> Product:
        inventory_data = validated_data.pop("inventory")
        category_data = validated_data.pop("category")
        discount_data = validated_data.pop("discount")

        inventory_instance = instance.inventory
        inventory_instance.quantity = inventory_data.get(
            "quantity", inventory_instance.quantity
        )
        inventory_instance.save()

        fields = ["name", "price", "weight", "short_description", "long_description"]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except (Error := KeyError):
                raise Error(f"{Error} : Missing data")

        instance.category, created = ProductCategory.objects.get_or_create(
            **category_data
        )
        instance.save()
        if discount_data:
            if percentage := discount_data.get("percentage", None):
                instance.set_discount(percentage)

        return instance


class ReviewService:
    @classmethod
    @transaction.atomic
    def create_review(cls, user: User, validated_data: dict) -> ProductReview:
        product_id = validated_data.pop("product_id")
        product_instance = get_object_or_404(Product, id=product_id)
        review = ProductReview.objects.create(
            user=user, product=product_instance, **validated_data
        )
        return review
