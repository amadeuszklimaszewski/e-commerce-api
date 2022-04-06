from django.http import QueryDict
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
    CartItemOutputSerializer,
    CartOutputSerializer,
    CouponInputSerializer,
    CouponOutputSerializers,
)
from src.apps.orders.services import CouponService
from src.apps.orders.permissions import OwnerOrAdmin


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


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.create(user=user)
        return Response(
            self.get_serializer(cart).data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> QueryDict:
        qs = self.queryset.filter(user=self.request.user)
        print(type(qs))
        return qs


class CartDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer
    permission_classes = [OwnerOrAdmin]
    lookup_field = "pk"


class CartItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer
    permission_classes = [OwnerOrAdmin]
    lookup_field = "pk"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return CartItem.objects.filter(cart_id=pk)

    def create(self, request, *args, **kwargs):
