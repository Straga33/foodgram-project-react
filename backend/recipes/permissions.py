from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка безопасные методы для всех,
    остальные для администратора."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_staff
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Проверка изменение только автором."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
