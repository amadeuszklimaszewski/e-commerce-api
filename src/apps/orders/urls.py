from django.urls import path
from src.apps.orders.views import (
    CartItemsListCreateAPIView,
    CartListCreateAPIView,
    CartDetailAPIView,
    CouponListCreateAPIView,
    CouponDetailAPIView,
)

urlpatterns = [
    path("coupons/", CouponListCreateAPIView.as_view()),
    path("coupons/<int:pk>/", CouponDetailAPIView.as_view()),
    path("carts/", CartListCreateAPIView.as_view()),
    path("carts/<int:pk>", CartDetailAPIView.as_view()),
    path("carts/<int:pk>/items/", CartItemsListCreateAPIView.as_view()),
]
