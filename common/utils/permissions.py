from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    """
    Base permission class to check if user has a specific role(s) or is staff/superuser.
    """
    allowed_roles = []  # Override in subclasses

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return getattr(user, 'role', None) in self.allowed_roles


class IsAdminOrHost(RolePermission):
    allowed_roles = ['admin', 'host']


class IsAdminRole(RolePermission):
    allowed_roles = ['admin']
