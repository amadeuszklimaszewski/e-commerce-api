from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("accounts/", include("src.apps.accounts.urls")),
]
