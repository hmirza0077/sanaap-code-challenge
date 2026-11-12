import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def fill_uuid(apps, schema_editor):
    # every existing document needs its own uuid before the field becomes unique
    Document = apps.get_model("documents", "Document")
    for document in Document.objects.all():
        document.uuid = uuid.uuid4()
        document.save(update_fields=["uuid"])


class Migration(migrations.Migration):
    # the data step (fill_uuid) and the schema steps run in separate transactions
    atomic = False

    dependencies = [
        ("documents", "0003_alter_document_file_storage"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(fill_uuid, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="document",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="document",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AddField(
            model_name="document",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="document",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="document",
            name="deleted_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("ready", "Ready"), ("failed", "Failed")],
                default="pending",
                max_length=10,
            ),
        ),
    ]
