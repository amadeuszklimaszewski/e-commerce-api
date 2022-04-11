from django.shortcuts import get_object_or_404

from src.apps.orders.models import Order
from src.apps.products.models import Product


def _update_product_inventory(order_instance):
    """
    Function takes in order instance as a parameter.
    It changes .sold attribute in each of order products after
    a successful payment.
    """
    order_items = order_instance.order_items.all()
    for orderitem in order_items:
        product_id = orderitem.product.id
        product = get_object_or_404(Product, id=product_id)
        product_inventory = product.inventory

        quantity = orderitem.quantity
        product_inventory.sold += quantity
        product_inventory.save()
    return


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
    _update_product_inventory(order)
    return
