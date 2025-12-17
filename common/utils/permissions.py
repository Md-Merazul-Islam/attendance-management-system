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
        return user.role.role_name in self.allowed_roles


class IsAdminRole(RolePermission):
    allowed_roles = ["admin"]


class IsEmployee(RolePermission):
    allowed_roles = ["Employee"]


class IsAdministrator(RolePermission):
    allowed_roles = ["Administrator"]
