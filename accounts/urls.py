from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from rest_framework.authtoken.views import obtain_auth_token  # Token auth (old)

from .views import MeView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    # --- JWT auth (current) ---
    path("login/", TokenObtainPairView.as_view(), name="login"),  # username + password -> access + refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),  # refresh -> new access
    # --- Token auth (old) - uncomment this and comment the two lines above to switch back ---
    # path("login/", obtain_auth_token, name="login"),  # username + password -> token
    path("me/", MeView.as_view(), name="me"),
] + router.urls
