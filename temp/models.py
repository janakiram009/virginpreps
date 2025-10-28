from django.db import models
from django.contrib.auth.models import User  # Optional: Link to auth users


class Vegetable(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Daily market price
    # Add quantity_available = models.IntegerField(default=0) if tracking stock

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Optional user link
    blacklisted_vegetables = models.ManyToManyField(
        Vegetable, blank=True
    )  # No-delivery list

    def __str__(self):
        return self.name
