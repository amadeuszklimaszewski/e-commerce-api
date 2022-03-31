from django.contrib.auth import get_user_model
from django.db import transaction

from src.apps.accounts.models import UserProfile, UserAddress

User = get_user_model()


class UserRegistrationService:
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
