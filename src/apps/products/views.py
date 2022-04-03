from pkg_resources import PkgResourcesDeprecationWarning
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.products.models import Product, ProductCategory, ProductInventory
from src.apps.products.serializers import (
    ProductCategoryListOutputSerializer,
    ProductInputSerializer,
    ProductInventoryInputSerializer,
    ProductCategoryInputSerializer,
    ProductListOutputSerializer,
    ProductDetailOutputSerializer,
)
from src.apps.products.services import ProductService


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListOutputSerializer
    permission_classes = [permissions.IsAuthenticated]
    service_class = ProductService

    def create(self, request, *args, **kwargs):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.service_class.create_product(serializer.validated_data)
        return Response(
            self.get_serializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailOutputSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"


class ProductCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryListOutputSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = ProductCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = ProductCategory.objects.create(**serializer.validated_data)
        return Response(
            self.get_serializer(category).data, status=status.HTTP_201_CREATED
        )
