from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name}-{self.pk}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, models.CASCADE, related_name='product')