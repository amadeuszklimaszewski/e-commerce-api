from rest_framework import permissions


class OwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow accessing own cart.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
