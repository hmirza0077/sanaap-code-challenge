import django.core.validators
from django.db import migrations, models

import common.utils

STATUS_CHOICES = [("pending", "Pending"), ("ready", "Ready")]


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        # documents that already exist have their file, so they start as "ready"
        migrations.AddField(
            model_name="document",
            name="status",
            field=models.CharField(choices=STATUS_CHOICES, default="ready", max_length=10),
        ),
        # new documents start as "pending"
        migrations.AlterField(
            model_name="document",
            name="status",
            field=models.CharField(choices=STATUS_CHOICES, default="pending", max_length=10),
        ),
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(
                blank=True,
                upload_to=common.utils.upload_document_prefix_helper,
                validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png"])],
            ),
        ),
    ]
