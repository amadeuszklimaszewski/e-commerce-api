from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_item_quantity(quantity, max_quantity):
    if quantity > max_quantity:
        raise ValidationError(
            _("%(quantity)s is larger quantity than the amount of products in stock."),
            params={"quantity": quantity},
        )
