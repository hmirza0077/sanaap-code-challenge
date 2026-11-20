from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend

from common.models import SoftDeleteModel
from common.utils import upload_document_prefix_helper
from documents import const

User = get_user_model()


class Document(SoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"  # file is waiting for the background worker
        READY = "ready", "Ready"  # file is stored in MinIO and can be downloaded
        FAILED = "failed", "Failed"  # all automatic retries failed; the user can retry from the API

    title = models.CharField(max_length=255)
    # empty until the background task stores the file in MinIO
    file = models.FileField(
        storage=MinioBackend(bucket_name=settings.MINIO_APP_PRIVATE_BUCKET),
        upload_to=upload_document_prefix_helper,
        validators=[FileExtensionValidator(const.ALLOWED_DOCUMENT_EXTENSIONS)],
        blank=True,
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="documents")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DocumentShare(SoftDeleteModel):
    """The owner shares a document with a user: that user can see and download it, but cannot change it."""

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_documents")
    shared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")

    class Meta:
        constraints = [
            # one active share per user and document; unshared (soft deleted) rows are kept as history
            models.UniqueConstraint(
                fields=["document", "user"],
                condition=models.Q(is_deleted=False),
                name="unique_active_document_share",
            ),
        ]

    def __str__(self):
        return f"{self.document} -> {self.user}"
