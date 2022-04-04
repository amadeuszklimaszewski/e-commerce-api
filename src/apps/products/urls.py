from django.urls import path

from src.apps.products.views import (
    ProductDetailAPIView,
    ProductListCreateAPIView,
    ProductCategoryListCreateAPIView,
    ProductReviewListCreateAPIView,
)

urlpatterns = [
    path("", ProductListCreateAPIView.as_view()),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("categories/", ProductCategoryListCreateAPIView.as_view()),
    path("reviews/", ProductReviewListCreateAPIView.as_view()),
]
