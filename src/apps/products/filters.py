from django import forms
from django.db.models import Case, When, F, Q, Value, Avg, Count
from django.db import models
from django_filters import rest_framework as filters
from src.apps.products.models import Product, ProductCategory, ProductReview


class ProductFilter(filters.FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        queryset=ProductCategory.objects.all(),
        field_name="category__name",
        to_field_name="name",
    )
    price = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        lookup_choices=[
            ("exact", "Equals"),
            ("gt", "Greater than"),
            ("lt", "Less than"),
        ],
    )
    uncategorized = filters.BooleanFilter(field_name="category", lookup_expr="isnull")
    discounted = filters.BooleanFilter(
        label="Is discounted",
        method="filter_is_discounted",
    )

    average_rating = filters.NumberFilter(
        label="Average rating equals", method="filter_average_rating"
    )
    average_rating__lt = filters.NumberFilter(
        label="Average rating lower than", method="filter_average_rating"
    )
    average_rating__gt = filters.NumberFilter(
        label="Average rating higher than", method="filter_average_rating"
    )

    class Meta:
        model = Product
        fields = [
            "category",
            "price",
        ]

    def filter_average_rating(self, queryset, name, value):
        if value is not None:
            queryset = queryset.annotate(
                average_rating=Avg("reviews__rating", distinct=True)
            )
            if name == "average_rating":
                queryset = queryset.filter(average_rating=value)
            if name == "average_rating__lt":
                queryset = queryset.filter(average_rating__lt=value)
            if name == "average_rating__gt":
                queryset = queryset.filter(average_rating__gt=value)
        return queryset

    def filter_is_discounted(self, queryset, name, value):
        if value is not None:
            queryset = queryset.annotate(
                discounted=Case(
                    When(price=F("discount_price"), then=False), default=True
                )
            ).filter(discounted=value)
        return queryset
