from django.urls import path

from src.apps.products.views import (
    ProductDetailAPIView,
    ProductListCreateAPIView,
    ProductCategoryListCreateAPIView,
    ProductReviewDetailAPIView,
    ProductReviewListCreateAPIView,
)

urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path(
        "categories/", ProductCategoryListCreateAPIView.as_view(), name="category-list"
    ),
    path("reviews/", ProductReviewListCreateAPIView.as_view(), name="review-list"),
    path(
        "reviews/<int:pk>/", ProductReviewDetailAPIView.as_view(), name="review-detail"
    ),
]
