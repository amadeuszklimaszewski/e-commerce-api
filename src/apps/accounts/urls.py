from django.urls import include, path
from .views import (
    AdressListCreateAPIView,
    RegistrationCreateAPIView,
    UserProfileListAPIView,
)

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
    path("registration/", RegistrationCreateAPIView.as_view()),
    path("addresses/", AdressListCreateAPIView.as_view()),
]
