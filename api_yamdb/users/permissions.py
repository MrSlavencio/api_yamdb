from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Полный доступ для администратора.
    Остальные роли доступ только для чтения.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """
    Полный доступ для администратора, модератора и автора.
    В остальных случаях доступ только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
