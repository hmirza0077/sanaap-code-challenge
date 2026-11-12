import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Django must be set up before importing code that uses models
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

from accounts.websocket_auth import JWTAuthMiddleware  # noqa: E402
from documents.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # normal API requests
        "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
