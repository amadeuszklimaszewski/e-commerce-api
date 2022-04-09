from django.urls import include, path
from django.conf import settings
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from src.apps.accounts.views import (
    AdressListCreateAPIView,
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileUpdateRetrieveAPIView,
)

urlpatterns = [
    path("users/", UserProfileListAPIView.as_view()),
    path(
        "users/<uuid:account_id>/",
        UserProfileUpdateRetrieveAPIView.as_view(),
        name="user-detail",
    ),
    path("register/", UserRegisterAPIView.as_view()),
    path("addresses/", AdressListCreateAPIView.as_view()),
    # dj-rest-auth
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("login/", LoginView.as_view(), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
]

if getattr(settings, "REST_USE_JWT", False):
    from rest_framework_simplejwt.views import TokenVerifyView
    from rest_framework_simplejwt.views import TokenObtainPairView
    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
