from rest_framework import permissions


class IsOwnerOrReadOnlyPublic(permissions.BasePermission):
    """
    Пользователь может:
    - редактировать/удалять ТОЛЬКО свои привычки;
    - просматривать публичные привычки других.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_published or obj.owner == request.user

        return obj.owner == request.user
