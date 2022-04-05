from rest_framework import permissions


class OwnCartPermission(permissions.BasePermission):
    """
    Object-level permission to only allow accessing own cart.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
