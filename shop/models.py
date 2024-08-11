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
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    quantity = models.IntegerField(default=1)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="shop/products/")
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.title
