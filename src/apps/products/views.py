from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.products.models import Product, ProductCategory, ProductInventory
from src.apps.products.serializers import (
    ProductInputSerializer,
    ProductInventoryInputSerializer,
    ProductCategoryInputSerializer,
    ProductListOutputSerializer,
    ProductDetailOutputSerializer,
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListOutputSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailOutputSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"
