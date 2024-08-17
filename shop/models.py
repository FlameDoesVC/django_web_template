import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.DO_NOTHING,
        related_name="items",
    )
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zip_code}"


class Order(models.Model):
    slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.DO_NOTHING)
    notes = models.TextField()
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Pending")

    def __str__(self):
        return f"Order {self.id}"

    @staticmethod
    def generate_slug():
        return uuid.uuid4()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name="items",
    )
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    image = models.ImageField(upload_to="shop/products/")
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
