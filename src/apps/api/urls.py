from django.urls import include, path


urlpatterns = [
    path("accounts/", include("src.apps.accounts.urls")),
    path("products/", include("src.apps.products.urls")),
]
