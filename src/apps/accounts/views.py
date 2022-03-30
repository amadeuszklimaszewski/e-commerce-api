from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
    allow_staff_view = True


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "accounts_id"


class RegistrationCreateAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]
