from django.contrib.auth import models as auth_models
from django.db import models

from common.models import SoftDeleteManager, SoftDeleteModel


class UserManager(SoftDeleteManager, auth_models.UserManager):
    """Django's UserManager (create_user, ...) without deleted users, so they cannot log in."""


class User(auth_models.AbstractUser, SoftDeleteModel):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Viewer"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)

    objects = UserManager()

    @property
    def is_admin_role(self):
        # superusers created with createsuperuser are treated as admin too
        return self.is_superuser or self.role == self.Role.ADMIN

    @property
    def is_editor_role(self):
        return self.role == self.Role.EDITOR
