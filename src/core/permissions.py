from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow actions not in SAFE_METHODS
    only for admin.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )
