from django import forms
from django.db.models import Case, When, F, Q, Value
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

    class Meta:
        model = Product
        fields = ["category", "price", "uncategorized"]
