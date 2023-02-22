from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj == request.user or request.user.is_staff
        elif request.method == 'POST':
            return True
        else:
            return False
