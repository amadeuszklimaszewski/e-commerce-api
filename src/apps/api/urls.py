from django.urls import include, path

from src.apps.payments.views import StripeWebhookView


urlpatterns = [
    path("accounts/", include("src.apps.accounts.urls", namespace="accounts")),
    path("products/", include("src.apps.products.urls", namespace="products")),
    path("", include("src.apps.orders.urls", namespace="orders")),
    path("stripe/webhook/", StripeWebhookView.as_view()),
]
