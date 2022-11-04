from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser)


class IsAdminOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in SAFE_METHODS or obj.author == user or user.is_superuser
