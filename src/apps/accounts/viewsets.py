from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .serializers import UserProfileSerializer, UserSerializer
from .models import UserProfile, UserProfileAddress


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class UserProfileViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "pk"
