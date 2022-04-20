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
from src.apps.payments.views import (
    StripeSessionView,
    StripeConfigView,
)

urlpatterns = [
    path("coupons/", CouponListCreateAPIView.as_view(), name="coupon-list"),
    path("coupons/<int:pk>/", CouponDetailAPIView.as_view(), name="coupon-detail"),
    path("carts/", CartListCreateAPIView.as_view(), name="cart-list"),
    path("carts/<int:pk>/", CartDetailAPIView.as_view(), name="cart-detail"),
    path(
        "carts/<int:pk>/items/",
        CartItemsListCreateAPIView.as_view(),
        name="cart-item-list",
    ),
    path(
        "carts/<int:pk>/items/<int:cart_item_pk>/",
        CartItemsDetailAPIView.as_view(),
        name="cart-item-detail",
    ),
    path("carts/<int:pk>/order/", OrderCreateAPIView.as_view(), name="create-order"),
    path("orders/", OrderListAPIView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("orders/<int:pk>/session/", StripeSessionView.as_view(), name="stripe-setup"),
    path("orders/stripe/", StripeConfigView.as_view(), name="stripe-detail"),
]
