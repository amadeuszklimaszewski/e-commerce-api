from django.urls import include, path
from .views import UserProfileListAPIView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("users/", UserProfileListAPIView.as_view()),
]
