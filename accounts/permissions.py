from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminRole(BasePermission):
    """Only users with the admin role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class DocumentPermission(BasePermission):
    """
    admin  -> every document, every action
    editor -> upload; update / share / retry only own documents; read documents shared with them
    viewer -> read only the documents shared with them
    Which documents a user can see at all is decided in DocumentViewSet.get_queryset.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False

        if request.method in SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return user.is_admin_role
        # POST / PUT / PATCH (upload, update, share, unshare, retry)
        return user.is_admin_role or user.is_editor_role

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # only the owner (or an admin) can change a document; a shared user can only read it
        return request.user.is_admin_role or obj.uploaded_by_id == request.user.id
