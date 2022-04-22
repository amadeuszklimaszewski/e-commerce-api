from django.urls import include, path


urlpatterns = [
    path("accounts/", include("src.apps.accounts.urls", namespace="accounts")),
    path("products/", include("src.apps.products.urls", namespace="products")),
    path("", include("src.apps.orders.urls")),
]
