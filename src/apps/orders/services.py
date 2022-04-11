from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from src.apps.accounts.models import UserAddress
from src.apps.orders.decorators import database_debug
from src.apps.orders.models import (
    Order,
    OrderItem,
    Cart,
    CartItem,
    Coupon,
)
from src.apps.orders.validators import validate_item_quantity, validate_coupon_total
from src.apps.products.models import Product

User = get_user_model()


class CouponService:
    """
    Service for creating and updating coupons.
    """

    @classmethod
    @transaction.atomic
    def update_coupon(cls, instance: Coupon, validated_data: dict) -> Coupon:
        fields = [
            "code",
            "amount",
            "is_active",
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except (Error := KeyError):
                raise Error(f"{Error} : Missing data")
        instance.save()
        return instance


class CartService:
    """
    Service for managing carts. Creating and updating cart items checks quantity
    available in product's inventory and in case of deficiency, raises ValidationError.
    When updating, if the quantity is equal to 0, it removes the item from the cart.
    """

    @classmethod
    @transaction.atomic
    def create_cart_item(cls, cart_id: int, validated_data: dict) -> CartItem:
        product_id = validated_data.pop("product_id")
        quantity = validated_data.pop("quantity")
        product_instance = get_object_or_404(Product, id=product_id)
        max_quantity = product_instance.inventory.quantity
        validate_item_quantity(quantity, max_quantity)
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
        except CartItem.DoesNotExist:
            product_instance = get_object_or_404(Product, id=product_id)
            cart_instance = get_object_or_404(Cart, id=cart_id)
            cartitem = CartItem.objects.create(
                cart=cart_instance,
                product=product_instance,
                quantity=quantity,
            )
            cartitem.save()
        return cartitem

    @classmethod
    def _check_quantity(cls, instance: CartItem, quantity: int):
        if quantity == 0:
            instance.delete()
            return False
        return True

    @classmethod
    @transaction.atomic
    def update_cart_item(cls, instance: CartItem, validated_data: dict):
        quantity = validated_data["quantity"]
        max_quantity = instance.product.inventory.quantity
        validate_item_quantity(quantity, max_quantity)
        if cls._check_quantity(instance, quantity):
            try:
                setattr(instance, "quantity", quantity)
            except KeyError as err:
                raise err(f"{err} : Missing or wrong data")
            instance.save()
            return instance
        return


class OrderService:
    """
    Service for managing orders. Creates an Order instance based on cart.
    With a successful operation, it lowers the available quantity of each Product
    and deletes the cart used to create an order.

    Optional coupons are checked if they exist, are active and
    the minimal total requirement is fulfilled.

    After a payment is confirmed by Stripe, StripeWebhookView calls .fullfill()
    method which updates quantity sold of each item and changes
    .payment_accepted attribute of an order to `True`.
    """

    @classmethod
    def _create_order_items(cls, order_instance: Order, cart_items):
        for cartitem in cart_items:
            product = cartitem.product
            quantity = cartitem.quantity
            max_quantity = product.inventory.quantity

            validate_item_quantity(quantity, max_quantity)

            OrderItem.objects.create(
                order=order_instance, product=product, quantity=quantity
            )
            inventory_instance = product.inventory
            inventory_instance.quantity = inventory_instance.quantity - quantity
            inventory_instance.save()
        return

    @classmethod
    @transaction.atomic
    @database_debug
    def create_order(cls, cart_id: int, user: User, validated_data) -> Order:

        address_instance = get_object_or_404(
            UserAddress, id=validated_data["address_id"], userprofile__user=user
        )
        cart_instance = get_object_or_404(Cart, id=cart_id, user=user)
        cart_items = cart_instance.cart_items.select_related(
            "product", "product__inventory"
        ).all()

        order = Order.objects.create(user=user, address=address_instance)

        cls._create_order_items(order_instance=order, cart_items=cart_items)

        if "coupon_code" in validated_data.keys():
            coupon = get_object_or_404(
                Coupon, code=validated_data["coupon_code"], is_active=True
            )
            validate_coupon_total(
                total=order.before_coupon, min_total=coupon.min_order_total
            )
            order.coupon = coupon
            order.save()
        cart_instance.delete()
        return order

    @classmethod
    @transaction.atomic
    def update_order(cls, instance: Order, user: User, validated_data) -> Order:
        if "coupon_code" in validated_data.keys():
            coupon = get_object_or_404(
                Coupon, code=validated_data["coupon_code"], is_active=True
            )
            validate_coupon_total(
                total=instance.before_coupon, min_total=coupon.min_order_total
            )
            instance.coupon = coupon
            instance.save()
        else:
            instance.coupon = None
            instance.save()

        instance.address = get_object_or_404(
            UserAddress, id=validated_data["address_id"], userprofile__user=user
        )
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def destroy_order(cls, instance: Order):
        orderitems = instance.order_items.select_related(
            "product", "product__inventory"
        ).all()
        for orderitem in orderitems:
            inventory_instance = orderitem.product.inventory
            inventory_instance.quantity += orderitem.quantity
            inventory_instance.save()
        instance.delete()
        return

    @classmethod
    @database_debug
    def _update_product_inventory(cls, order_instance: Order):
        order_items = order_instance.order_items.select_related(
            "product", "product__inventory"
        ).all()
        for orderitem in order_items:
            product_id = orderitem.product.id
            product = get_object_or_404(Product, id=product_id)
            product_inventory = product.inventory

            quantity = orderitem.quantity
            product_inventory.sold += quantity
            product_inventory.save()
        return

    @classmethod
    @transaction.atomic
    def fullfill_order(cls, session):
        order_id = session["metadata"]["order_id"]
        order = get_object_or_404(Order, id=order_id)
        order.order_accepted = True
        order.payment_accepted = True
        order.save()
        cls._update_product_inventory(order)
        return
