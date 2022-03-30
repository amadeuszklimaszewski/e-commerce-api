from django.urls import include, path
from .views import RegistrationCreateAPIView, UserProfileListAPIView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
    path("registration/", RegistrationCreateAPIView.as_view()),
]
