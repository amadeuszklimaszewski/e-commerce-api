from django.db import models

# from django.template.defaultfilters import slugify
# from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class ProductInventory(models.Model):
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    @property
    def get_availability(self) -> str:
        pass

    def __str__(self) -> str:
        return f"Available stock : {self.quantity} || {self.product.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)

    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    short_description = models.CharField(max_length=1000, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    # TODO research about most optimal way of serving and storing images
    # image = models.FieldFile()
    # TODO research about slugs and consider implementing them
    # slug = models.SlugField(max_length=100, null=False, unique=True)

    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    inventory = models.OneToOneField(
        ProductInventory, on_delete=models.CASCADE, related_name="product"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def set_discount(self, percentage: float):
        self.discount_price = self.price * (1 - percentage)
        self.save()

    @property
    def is_discounted(self) -> bool:
        return bool(self.discount_price)

    def remove_discount(self):
        self.discount_price = None
        self.save()

    def get_absolute_url(self) -> str:
        return f"/api/products/{self.pk}/"

    @property
    def endpoint(self) -> str:
        return self.get_absolute_url()

    # def get_absolute_url(self):
    #     kwargs = {"slug": self.slug}
    #     return reverse("product_detail", kwargs=kwargs)

    def __str__(self) -> str:
        return self.name
