from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from src.apps.accounts.models import UserProfile, UserAddress

User = get_user_model()


class UserProfileService:
    """
    Service used for registration of a User.
    Creates instances of User, Address and UserProfile
    with validated data and links them together.
    """

    @classmethod
    def _create_user(cls, data: dict) -> User:
        user = User.objects.create(**data)
        return user

    @classmethod
    def _create_address(cls, data: dict) -> UserAddress:
        address = UserAddress.objects.create(**data)
        return address

    @classmethod
    @transaction.atomic
    def register_user(cls, validated_data: dict) -> UserProfile:
        user_data = validated_data.pop("user")
        address_data = validated_data.pop("address")

        user = cls._create_user(user_data)
        address = cls._create_address(address_data)

        user_profile = UserProfile.objects.create(user=user, **validated_data)
        user_profile.address.add(address)
        return user_profile

    @classmethod
    def _update_user(cls, user_instance: User, user_data: dict) -> User:
        user_instance.first_name = user_data.get("first_name", user_instance.first_name)
        user_instance.last_name = user_data.get("last_name", user_instance.last_name)
        user_instance.email = user_data.get("email", user_instance.email)
        user_instance.save()
        return user_instance

    @classmethod
    def _update_address(cls, address_data: list) -> UserAddress:
        address_ids = []
        for address in address_data:
            address_instance, created = UserAddress.objects.update_or_create(
                pk=address.get("id"), defaults=address
            )
            address_ids.append(address_instance.pk)
        return address_ids

    @classmethod
    @transaction.atomic
    def update_user(cls, instance: UserProfile, validated_data: dict) -> UserProfile:
        user_data = validated_data.pop("user")
        address_data = validated_data.pop("address", [])

        user_instance = instance.user
        cls._update_user(user_instance, user_data)

        instance.address.set(cls._update_address(address_data))

        fields = ["phone_number", "birthday"]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except (Error := KeyError):
                raise Error(f"{Error} : Missing data")
        instance.save()

        # Removal of addresses not related to any UserProfile object
        addresses = set(UserProfile.objects.all().values_list("address", flat=True))
        addresses.discard(None)
        UserAddress.objects.filter(~Q(id__in=addresses)).delete()

        return instance
