from django.urls import path

from src.apps.products.views import ProductDetailAPIView, ProductListCreateAPIView

urlpatterns = [
    path("", ProductListCreateAPIView.as_view()),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
