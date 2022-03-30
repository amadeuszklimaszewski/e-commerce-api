from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class UserAddress(models.Model):
    address_1 = models.CharField(max_length=150, blank=True, null=True)
    address_2 = models.CharField(max_length=150, blank=True, null=True)
    country = CountryField()
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=16)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"Address: {self.address_1}, {self.city}, {self.country}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = PhoneNumberField()
    birthday = models.DateField()
    address = models.ManyToManyField(UserAddress)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self) -> str:
        return f"Profile of the user: {self.user.username}"
