from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from src.apps.accounts.models import UserAddress, UserProfile
from src.apps.accounts.serializers import (
    RegistrationInputSerializer,
    UserAddressOutputSerializer,
    UserProfileListOutputSerializer,
    UserProfileDetailOutputSerializer,
    RegistrationOutputSerializer,
)
from src.apps.accounts.services import UserRegistrationService


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListOutputSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailOutputSerializer
    lookup_field = "account_id"


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = RegistrationOutputSerializer
    permission_classes = [permissions.AllowAny]
    service_class = UserRegistrationService

    def create(self, request, *args, **kwargs):
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = self.service_class.register_user(serializer.validated_data)
        # user=request.user
        return Response(
            self.get_serializer(user_profile).data,
            status=status.HTTP_201_CREATED,
        )


class AdressListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressOutputSerializer
    permission_classes = [permissions.IsAuthenticated]
