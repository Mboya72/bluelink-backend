from rest_framework import permissions

class IsFisherman(permissions.BasePermission):
    """
    Allows access only to users with the 'FISHERMAN' role.
    """
    def has_permission(self, request, view):
        # This assumes you have a 'role' field or 'user_type' on your User model
        return bool(request.user and request.user.is_authenticated and request.user.role == 'FISHERMAN')