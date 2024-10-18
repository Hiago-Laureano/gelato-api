from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class UserIsOwnerOrIsSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            (request.user.id == obj.id) or
            (request.user and request.user.is_superuser)
        )