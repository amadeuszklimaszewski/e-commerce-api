from pkg_resources import PkgResourcesDeprecationWarning
from rest_framework import serializers
from src.apps.products.models import ProductCategory, ProductInventory, Product


class ProductCategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductInventoryInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(initial=0, allow_null=True)


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField(default=0, allow_null=True)
    weight = serializers.FloatField(default=0, allow_null=True, required=False)
    short_description = serializers.CharField(required=False)
    long_description = serializers.CharField(required=False)

    category = ProductCategoryInputSerializer(many=False)
    inventory = ProductInventoryInputSerializer(many=False, required=True)


class ProductCategoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name",)
        read_only_fields = fields


class ProductInventoryOutputSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ProductInventory
        fields = ("quantity", "updated")
        read_only_fields = fields


class ProductListOutputSerializer(serializers.ModelSerializer):
    inventory = ProductInventoryOutputSerializer(many=False, read_only=True)
    category = ProductCategoryOutputSerializer(many=False, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk"
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "inventory",
            "category",
            "endpoint",
            "url",
        )
        read_only_fields = fields


class ProductDetailOutputSerializer(serializers.ModelSerializer):
    inventory = ProductInventoryOutputSerializer(many=False, read_only=True)
    category = ProductCategoryOutputSerializer(many=False, read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "short_description",
            "long_description",
            "price",
            "weight",
            "inventory",
            "category",
            "created",
            "updated",
        )
        read_only_fields = fields


class ProductInlineOutputSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(source="inventory.quantity", read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk"
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "quantity",
            "endpoint",
            "url",
        )


class ProductCategoryListOutputSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    products = ProductInlineOutputSerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ("name", "description", "created", "updated", "products")
        read_only_fields = fields
