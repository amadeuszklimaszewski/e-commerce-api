from django.urls import path
from django.conf import settings
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from src.apps.accounts.views import (
    AdressListCreateAPIView,
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileDetailAPIView,
)

urlpatterns = [
    path("users/", UserProfileListAPIView.as_view()),
    path(
        "users/<uuid:account_id>/",
        UserProfileDetailAPIView.as_view(),
        name="user-detail",
    ),
    path("register/", UserRegisterAPIView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("addresses/", AdressListCreateAPIView.as_view()),
]

if getattr(settings, "REST_USE_JWT", False):
    from rest_framework_simplejwt.views import TokenVerifyView
    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
