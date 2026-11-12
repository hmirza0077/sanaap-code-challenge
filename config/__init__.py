# load Celery when Django starts, so tasks can be sent with .delay()
from .celery import app as celery_app

__all__ = ("celery_app",)
