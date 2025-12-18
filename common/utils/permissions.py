from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    """
    Base permission class to check if user has a specific role(s) or is staff/superuser.
    """

    allowed_roles = []  

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return user.role.role_name in self.allowed_roles

class IsAdmin(RolePermission):
    allowed_roles = ["Admin"]

class IsEmployee(RolePermission):
    allowed_roles = ["Employee"]


class IsAdministrator(RolePermission):
    allowed_roles = ["Administrator"]


class IsCompanyAdministrator(IsAdministrator):
    """
    Administrator who is assigned to a company
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.company is not None
