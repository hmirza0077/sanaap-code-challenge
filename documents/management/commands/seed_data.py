import base64
from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from documents.models import Document

PASSWORD = "pass12345"

# a tiny valid 1x1 PNG image, used as the content of every sample document
SAMPLE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

USERS = [
    ("admin", User.Role.ADMIN),
    ("sara_admin", User.Role.ADMIN),
    ("ali_editor", User.Role.EDITOR),
    ("reza_editor", User.Role.EDITOR),
    ("maryam_editor", User.Role.EDITOR),
    ("nima_viewer", User.Role.VIEWER),
    ("zahra_viewer", User.Role.VIEWER),
]

# (title, uploader, how many days ago it was created)
DOCUMENTS = [
    ("Invoice January", "ali_editor", 300),
    ("Invoice February", "ali_editor", 270),
    ("Invoice March", "reza_editor", 240),
    ("Invoice April", "reza_editor", 210),
    ("Contract - Office Rent", "admin", 200),
    ("Contract - Internet Provider", "sara_admin", 180),
    ("Contract - Cleaning Service", "maryam_editor", 150),
    ("ID Card Scan", "maryam_editor", 120),
    ("Passport Scan", "maryam_editor", 119),
    ("Insurance Policy Car", "ali_editor", 100),
    ("Insurance Policy Health", "ali_editor", 95),
    ("Insurance Claim Photo 1", "reza_editor", 60),
    ("Insurance Claim Photo 2", "reza_editor", 60),
    ("Insurance Claim Photo 3", "reza_editor", 59),
    ("Receipt Taxi", "maryam_editor", 45),
    ("Receipt Hotel", "maryam_editor", 40),
    ("Receipt Restaurant", "ali_editor", 30),
    ("Team Photo", "sara_admin", 20),
    ("Office Floor Plan", "admin", 15),
    ("Invoice October", "ali_editor", 10),
    ("Invoice November", "reza_editor", 5),
    ("Contract - New Supplier", "admin", 3),
    ("Meeting Whiteboard", "maryam_editor", 1),
    ("Signature Sample", "sara_admin", 0),
    ("Logo Draft", "ali_editor", 0),
]


class Command(BaseCommand):
    help = "Fill the database with sample users and documents for manual testing."

    def handle(self, *args, **options):
        users = self.create_users()
        self.create_documents(users)
        self.stdout.write(self.style.SUCCESS(f"Done. Password for every user: {PASSWORD}"))

    def create_users(self):
        users = {}
        for username, role in USERS:
            user, created = User.objects.get_or_create(username=username, defaults={"role": role})
            if created:
                user.set_password(PASSWORD)
                user.save()
            users[username] = user
            self.stdout.write(f"user: {username:15} role: {user.role}")
        return users

    def create_documents(self, users):
        if Document.objects.exists():
            self.stdout.write("Documents already exist, skipping.")
            return

        now = timezone.now()
        for title, username, days_ago in DOCUMENTS:
            document = Document(title=title, uploaded_by=users[username], status=Document.Status.READY)
            document.file.save("sample.png", ContentFile(SAMPLE_PNG), save=True)

            # created_at uses auto_now_add, so we change it after saving to get different dates
            Document.objects.filter(pk=document.pk).update(created_at=now - timedelta(days=days_ago))

        self.stdout.write(f"{len(DOCUMENTS)} documents created.")
