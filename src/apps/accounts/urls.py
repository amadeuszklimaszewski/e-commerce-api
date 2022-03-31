from django.urls import include, path
from .views import (
    AdressListCreateAPIView,
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileRetrieveAPIView,
)

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
    path(
        "users/<uuid:account_id>/",
        UserProfileRetrieveAPIView.as_view(),
        name="user-detail",
    ),
    path("registration/", UserRegisterAPIView.as_view()),
    path("addresses/", AdressListCreateAPIView.as_view()),
]
