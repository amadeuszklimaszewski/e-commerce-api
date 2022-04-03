from django.db import transaction
from src.apps.products.models import ProductCategory, ProductInventory, Product


class ProductService:
    """
    Service used for creating a product.
    """

    @classmethod
    @transaction.atomic
    def create_product(cls, validated_data: dict) -> Product:
        inventory_data = validated_data.pop("inventory")
        category_data = validated_data.pop("category")
        print(inventory_data)
        print(category_data)
        print(validated_data)
        inventory = ProductInventory.objects.create(**inventory_data)
        category, created = ProductCategory.objects.get_or_create(**category_data)

        product = Product.objects.create(
            inventory=inventory, category=category, **validated_data
        )
        return product
