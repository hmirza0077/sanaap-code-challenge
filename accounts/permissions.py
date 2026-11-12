from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminRole(BasePermission):
    """Only users with the admin role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class DocumentPermission(BasePermission):
    """
    admin  -> everything
    editor -> read, create, update (no delete)
    viewer -> read only
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False

        if request.method in SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return user.is_admin_role
        # POST / PUT / PATCH
        return user.is_admin_role or user.is_editor_role
