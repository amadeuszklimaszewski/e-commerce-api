from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter
from src.apps.accounts.viewsets import UserViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    re_path(r"^", include(router.urls)),
]

urlpatterns += [path("", include("rest_framework.urls"))]
