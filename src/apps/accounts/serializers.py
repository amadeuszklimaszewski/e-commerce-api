from django.contrib.auth.models import User
from rest_framework import serializers, status
from .models import UserProfile, UserProfileAdress


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """

    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "account_id",
            "phone_number",
            "birthday",
            "address",
            "created",
            "updated",
        )

    # def create(self, validated_data):
    #     """
    #     Overriding the default create method of the Model serializer.
    #     :param validated_data: data containing all the details of student
    #     :return: returns a successfully created student record
    #     """
    #     user_data = validated_data.pop("user")
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     student, created = UserProfile.objects.update_or_create(
    #         user=user, subject_major=validated_data.pop("subject_major")
    #     )
    #     return student
