from django.urls import path
from src.apps.orders.views import CouponListCreateAPIView, CouponDetailAPIView

urlpatterns = [
    path("coupons/", CouponListCreateAPIView.as_view()),
    path("coupons/<int:pk>/", CouponDetailAPIView.as_view()),
]
