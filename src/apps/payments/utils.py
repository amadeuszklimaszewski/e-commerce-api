from django.shortcuts import get_object_or_404

from src.apps.orders.models import Order


def fullfill_order(session):
    """
    Function takes in session instance as a parameter, retrieves
    Order instance given by order_id in metadata dict and changes
    its .payment_accepted attribute to True.
    """
    order_id = session["metadata"]["order_id"]
    order = get_object_or_404(Order, id=order_id)
    order.order_accepted = True
    order.payment_accepted = True
    order.save()
    return
