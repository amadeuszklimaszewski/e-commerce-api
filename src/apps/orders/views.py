from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.orders.models import (
    Order,
    Cart,
    CartItem,
    Coupon,
)
from src.apps.orders.serializers import (
    CartItemInputSerializer,
    CartItemOutputSerializer,
    CartItemQuantityInputSerializer,
    CartOutputSerializer,
    CouponInputSerializer,
    CouponOutputSerializers,
    OrderInputSerializer,
    OrderOutputSerializer,
)
from src.apps.orders.services import CartService, CouponService, OrderService
from src.apps.orders.permissions import CartOwnerOrAdmin


class CouponListCreateAPIView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponOutputSerializers

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_superuser:
            return qs
        return qs.none()

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
    service_class = CouponService

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_superuser:
            return qs
        return qs.none()

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

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.create(user=user)
        return Response(
            self.get_serializer(cart).data,
            status=status.HTTP_201_CREATED,
        )


class CartDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)


class CartItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer
    permission_classes = [CartOwnerOrAdmin]
    service_class = CartService

    def get_queryset(self):
        cart_pk = self.kwargs.get("pk")
        qs = self.queryset
        return qs.filter(cart_id=cart_pk, cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_id = self.kwargs.get("pk")
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cartitem = self.service_class.create_cart_item(
            cart_id, serializer.validated_data
        )
        return Response(
            self.get_serializer(cartitem).data,
            status=status.HTTP_201_CREATED,
        )


class CartItemsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer
    service_class = CartService

    def get_object(self):
        id = self.kwargs.get("cart_item_pk")
        cart_id = self.kwargs.get("pk")
        user = self.request.user
        obj = get_object_or_404(CartItem, id=id, cart_id=cart_id, cart__user=user)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        cartitem_instance = self.get_object()
        serializer = CartItemQuantityInputSerializer(
            instance=cartitem_instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        cartitem = self.service_class.update_cart_item(
            cartitem_instance, serializer.validated_data
        )
        return Response(
            self.get_serializer(cartitem).data,
            status=status.HTTP_200_OK,
        )


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer
    service_class = OrderService

    def create(self, request, *args, **kwargs):
        cart_id = kwargs.get("pk")
        serializer = OrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.service_class.create_order(
            cart_id=cart_id,
            user=self.request.user,
            validated_data=serializer.validated_data,
        )
        return Response(
            self.get_serializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer
    service_class = OrderService

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.order_accepted:
            return Response(
                {"order_accepted": "Order already accepted and paid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = OrderInputSerializer(
            instance=instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        updated_product = self.service_class.update_order(
            instance, self.request.user, serializer.validated_data
        )
        return Response(
            self.get_serializer(updated_product).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.service_class.destroy_order(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
