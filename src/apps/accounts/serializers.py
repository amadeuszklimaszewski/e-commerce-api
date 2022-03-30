from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UserAddress, UserProfile


User = get_user_model()


class UserInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )
    email = serializers.EmailField(
        # TODO move to services.py
        # validators=[
        #     UniqueValidator(
        #         queryset=User.objects.all(), message="Email already in use!"
        #     )
        #
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = (
            "address_1",
            "address_2",
            "country",
            "state",
            "city",
            "postalcode",
        )


class UserProfileListOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(many=False, required=True)
    address = UserAddressSerializer(many=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="user-detail", lookup_field="account_id"
    )

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "account_id",
            "address",
            "endpoint",
            "url",
        )


class UserDetailOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(many=False, required=True)
    address = UserAddressSerializer(many=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "account_id",
            "endpoint",
            "phone_number",
            "birthday",
            "address",
            "created",
            "updated",
        )


class RegistrationInputSerializer(serializers.ModelSerializer):

    user = UserInputSerializer(many=False, required=True)
    address = UserAddressSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "phone_number",
            "birthday",
            "address",
        )
