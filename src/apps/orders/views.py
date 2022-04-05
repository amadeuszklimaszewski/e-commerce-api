from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.orders.models import (
    Order,
    OrderItem,
    Cart,
    CartItem,
    Coupon,
)
from src.apps.orders.serializers import (
    CouponInputSerializer,
    CouponOutputSerializers,
)
from src.apps.orders.services import CouponService


class CouponListCreateAPIView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponOutputSerializers
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = CouponInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = Coupon.objects.create(**serializer.validated_data)
        return Response(
            self.get_serializer(coupon).data,
            status=status.HTTP_201_CREATED,
        )


class CouponDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponOutputSerializers
    permission_classes = [permissions.IsAdminUser]
    service_class = CouponService
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CouponInputSerializer(
            instance=instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        coupon = self.service_class.update_coupon(instance, serializer.validated_data)
        return Response(
            self.get_serializer(coupon).data,
            status=status.HTTP_200_OK,
        )
