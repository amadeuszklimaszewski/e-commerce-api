from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.accounts.models import UserAddress, UserProfile
from src.apps.accounts.serializers import (
    RegistrationInputSerializer,
    UserAddressOutputSerializer,
    UserProfileListOutputSerializer,
    UserProfileDetailOutputSerializer,
    RegistrationOutputSerializer,
    UserProfileUpdateInputSerializer,
)
from src.apps.accounts.services import UserProfileService


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailOutputSerializer
    service_class = UserProfileService
    lookup_field = "account_id"

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileUpdateInputSerializer(
            instance=instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        updated_userprofile = self.service_class.update_user(
            instance=instance, data=serializer.validated_data
        )
        return Response(
            self.get_serializer(updated_userprofile).data, status=status.HTTP_200_OK
        )


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = RegistrationOutputSerializer
    permission_classes = [permissions.AllowAny]
    service_class = UserProfileService

    def create(self, request, *args, **kwargs):
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = self.service_class.register_user(data=serializer.validated_data)
        return Response(
            self.get_serializer(user_profile).data,
            status=status.HTTP_201_CREATED,
        )


class AdressListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(userprofile__user=user)
