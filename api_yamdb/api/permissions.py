from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user.is_authenticated and user.is_staff
            or user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated and user.is_user
                or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'DELETE' and user.is_moderator:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            user.is_authenticated and user.is_staff
            or user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_user
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthorModAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        return (obj.author == request.user or 'moderator' == request.user.role
                or 'admin' == request.user.role)
