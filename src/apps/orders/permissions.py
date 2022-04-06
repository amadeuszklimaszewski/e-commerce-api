from rest_framework import permissions

from src.apps.orders.models import Cart, CartItem


class OwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow accessing own cart.
    """

    def has_object_permission(self, request, view, obj: Cart):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class CartOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: CartItem):
        if request.user.is_superuser:
            return True
        return obj.cart.user == request.user
