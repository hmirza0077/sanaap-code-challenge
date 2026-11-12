import django.core.validators
import django_minio_backend.models
from django.db import migrations, models

import common.utils


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0002_document_status"),
    ]

    operations = [
        # files are stored in the private MinIO bucket
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(
                blank=True,
                storage=django_minio_backend.models.MinioBackend(bucket_name="sanaap-private"),
                upload_to=common.utils.upload_document_prefix_helper,
                validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png"])],
            ),
        ),
    ]
