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
    Service used for creating a product.
    """

    @classmethod
    @transaction.atomic
    def create_product(cls, validated_data: dict) -> Product:
        inventory_data = validated_data.pop("inventory")
        category_data = validated_data.pop("category")

        inventory = ProductInventory.objects.create(**inventory_data)
        category, created = ProductCategory.objects.get_or_create(**category_data)

        product = Product.objects.create(
            inventory=inventory, category=category, **validated_data
        )
        return product

    @classmethod
    @transaction.atomic
    def update_product(cls, instance: Product, validated_data: dict) -> Product:
        inventory_data = validated_data.pop("inventory")
        category_data = validated_data.pop("category")

        inventory_instance = instance.inventory
        inventory_instance.quantity = inventory_data.get(
            "quantity", inventory_instance.quantity
        )
        inventory_instance.save()

        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.short_description = validated_data.get(
            "short_description", instance.short_description
        )
        instance.long_description = validated_data.get(
            "long_description", instance.long_description
        )
        instance.category, created = ProductCategory.objects.get_or_create(
            **category_data
        )
        instance.save()
        return instance


class ReviewService:
    @classmethod
    @transaction.atomic
    def create_review(cls, user: User, validated_data: dict) -> ProductReview:
        product_name = validated_data.pop("product_name")
        product_instance = get_object_or_404(Product, name=product_name)
        ProductReview.objects.create(
            user=user, product=product_instance, **validated_data
        )
