from django.urls import path

from src.apps.products.views import (
    ProductDetailAPIView,
    ProductListCreateAPIView,
    ProductCategoryListCreateAPIView,
    ProductCategoryDetailAPIView,
    ProductReviewListCreateAPIView,
    ProductReviewDetailAPIView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path(
        "categories/", ProductCategoryListCreateAPIView.as_view(), name="category-list"
    ),
    path(
        "categories/<int:pk>/",
        ProductCategoryDetailAPIView.as_view(),
        name="category-detail",
    ),
    path("reviews/", ProductReviewListCreateAPIView.as_view(), name="review-list"),
    path(
        "reviews/<int:pk>/", ProductReviewDetailAPIView.as_view(), name="review-detail"
    ),
]
