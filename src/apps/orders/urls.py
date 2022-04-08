from django.urls import path
from src.apps.orders.views import (
    CartItemsDetailAPIView,
    CartItemsListCreateAPIView,
    CartListCreateAPIView,
    CartDetailAPIView,
    CouponListCreateAPIView,
    CouponDetailAPIView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    OrderListAPIView,
)

urlpatterns = [
    path("coupons/", CouponListCreateAPIView.as_view()),
    path("coupons/<int:pk>/", CouponDetailAPIView.as_view()),
    path("carts/", CartListCreateAPIView.as_view()),
    path("carts/<int:pk>", CartDetailAPIView.as_view()),
    path("carts/<int:pk>/items/", CartItemsListCreateAPIView.as_view()),
    path("carts/<int:pk>/items/<int:cart_item_pk>/", CartItemsDetailAPIView.as_view()),
    path("carts/<int:pk>/order", OrderCreateAPIView.as_view()),
    path("orders/", OrderListAPIView.as_view()),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view()),
]
