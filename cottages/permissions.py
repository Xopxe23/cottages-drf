from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать только свой собственный объект.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения только для чтения, если это запрос на метод GET, HEAD или OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Пользователь может редактировать объект только если он является владельцем
        return obj.owner == request.user
