from django.db import models

from shop_admin.models import User

# Create your models here.
class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Product(models.Model):
		title = models.CharField(max_length=255)
		description = models.TextField()
		price = models.DecimalField(max_digits=6, decimal_places=2)
		image = models.ImageField(upload_to="products/")

		def __str__(self):
				return self.title