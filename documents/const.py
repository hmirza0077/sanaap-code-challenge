from datetime import timedelta

ALLOWED_DOCUMENT_EXTENSIONS = ["jpg", "jpeg", "png"]

# Download: the presigned MinIO link is valid only for a short time, so a shared link expires quickly
DOWNLOAD_URL_EXPIRY = timedelta(seconds=60)

# Background storage
PENDING_FILE_TIMEOUT = 24 * 60 * 60  # the uploaded file is kept in Redis for 1 day, so a failed upload can be retried
STORE_FILE_MAX_RETRIES = 3  # automatic retries of the Celery task before the document is marked as failed
STORE_FILE_RETRY_DELAY = 10  # seconds between automatic retries

# WebSocket: every user has an own group (see notifications.user_group_name); admins share one group
ADMINS_GROUP_NAME = "documents_admins"
DOCUMENT_EVENT_CREATED = "created"
DOCUMENT_EVENT_UPDATED = "updated"
