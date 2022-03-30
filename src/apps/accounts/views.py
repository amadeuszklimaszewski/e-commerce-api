from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .models import UserAddress, UserProfile
from .serializers import (
    RegistrationInputSerializer,
    UserAddressSerializer,
    UserProfileListOutputSerializer,
    UserDetailOutputSerializer,
)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListOutputSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailOutputSerializer
    lookup_field = "account_id"


class RegistrationCreateAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegistrationInputSerializer
    permission_classes = [permissions.AllowAny]


class AdressListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
