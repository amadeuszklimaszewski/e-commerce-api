from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

# from src.apps.accounts.viewsets import UserViewSet, UserProfileViewSet


# router = DefaultRouter()
# router.register(r"profiles", UserProfileViewSet)

urlpatterns = [
    path("accounts/", include("src.apps.accounts.urls")),
    # re_path(r"^", include(router.urls)),
]
