from django.urls import include, path
from .views import (
    AdressListCreateAPIView,
    RegistrationCreateAPIView,
    UserProfileListAPIView,
    UserProfileRetrieveUpdateAPIView,
)

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
    path(
        "users/<uuid:account_id>/",
        UserProfileRetrieveUpdateAPIView.as_view(),
        name="user-detail",
    ),
    path("registration/", RegistrationCreateAPIView.as_view()),
    path("addresses/", AdressListCreateAPIView.as_view()),
]
