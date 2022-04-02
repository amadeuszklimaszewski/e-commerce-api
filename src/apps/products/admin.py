from django.contrib import admin

from src.apps.products.models import Product, ProductCategory, ProductInventory

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductInventory)
admin.site.register(ProductCategory)
