from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.products.models import (
    Product,
    ProductCategory,
    ProductInventory,
    ProductReview,
)
from src.apps.products.serializers import (
    ProductCategoryListOutputSerializer,
    ProductInputSerializer,
    ProductCategoryInputSerializer,
    ProductListOutputSerializer,
    ProductDetailOutputSerializer,
    ProductReviewInputSerializer,
    ProductReviewOutputSerializer,
)
from src.apps.products.services import ProductService, ReviewService
from src.core.permissions import AdminOrReadOnly


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListOutputSerializer
    permission_classes = [AdminOrReadOnly]
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
    permission_classes = [AdminOrReadOnly]
    service_class = ProductService

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductInputSerializer(
            instance=instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        updated_product = self.service_class.update_product(
            instance, serializer.validated_data
        )
        return Response(
            self.get_serializer(updated_product).data,
            status=status.HTTP_200_OK,
        )


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


class ProductReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewOutputSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service_class = ReviewService

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = ProductReviewInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = self.service_class.create_review(user, serializer.validated_data)
        return Response(
            self.get_serializer(review).data, status=status.HTTP_201_CREATED
        )
