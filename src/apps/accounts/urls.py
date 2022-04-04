from django.urls import include, path
from .views import (
    AdressListCreateAPIView,
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileUpdateRetrieveAPIView,
)

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
    path(
        "users/<uuid:account_id>/",
        UserProfileUpdateRetrieveAPIView.as_view(),
        name="user-detail",
    ),
    path("registration/", UserRegisterAPIView.as_view()),
    path("addresses/", AdressListCreateAPIView.as_view()),
]
