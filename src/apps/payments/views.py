from django.shortcuts import get_object_or_404

from decouple import config
import stripe

from rest_framework import status, views, permissions
from rest_framework.response import Response

from src.apps.orders.models import Order
from src.apps.orders.services import OrderService
from src.core.authentication import CsrfExemptSessionAuthentication


stripe.api_key = config("STRIPE_SECRET_KEY")


class StripeConfigView(views.APIView):
    """
    StripeConfigView returns Stripe's publishable_key on GET.
    """

    def get(self, request, format=None):
        data = {"publishable_key": str(config("STRIPE_PUBLISHABLE_KEY"))}
        return Response(data, status=status.HTTP_200_OK)


class StripeSessionView(views.APIView):
    """
    StripeSessionView creates stripe.checkout instance and returns
    sessionId on GET.
    """

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(Order, id=order_id)
        if order.payment_accepted:
            return Response(
                {"payment": "Payment already accepted"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        price_data = {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Order #{order.id}",
                },
                "unit_amount": int(order.total * 100),
            },
            "quantity": 1,
        }

        checkout_session = stripe.checkout.Session.create(
            success_url=config("PAYMENT_SUCCESS_URL"),
            cancel_url=config("PAYMENT_CANCEL_URL"),
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                price_data,
            ],
            metadata={"order_id": order_id},
        )
        return Response(
            {"sessionId": checkout_session["id"]}, status=status.HTTP_200_OK
        )


class StripeWebhookView(views.APIView):
    """
    StripeWebhookView is responsible of handling the webhook
    events of /webhook/ endpoint. After succesful payment,
    the .payment_accepted attribute of Order instance is changed
    to True.
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]
    service_class = OrderService

    def post(self, request, format=None):
        endpoint_secret = config("WEBHOOK_SECRET")
        payload = request.body.decode("utf-8")
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            print(event["data"]["object"]["payment_intent"])
            session = event["data"]["object"]
            self.service_class.fullfill_order(session)
            print(session["metadata"]["order_id"])

        return Response(status=status.HTTP_200_OK)
