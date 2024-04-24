from django import forms
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    material = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customers = models.ManyToManyField(Customer, related_name='cart', blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):

        self.name = f"{self.color} {self.material} {self.item_type}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def serialize(self):
        """
        Serialize product details into a dictionary.
        """
        return {
            'id': self.id,
            'material': self.material,
            'color': self.color,
            'item_type': self.item_type,
            'stock': self.stock,
            'image_url': self.image_url,
            'price': str(self.price),
            'name': self.name,
            'user_id': self.user.id if self.user else None,
            'quantity': self.quantity,
        }



class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    purchase_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255, null=True)
    card_credentials = models.CharField(max_length=16, null=True)
    expiry_month = models.CharField(max_length=2, null=True)
    expiry_year = models.CharField(max_length=2, null=True)
    cvc = models.CharField(max_length=3, null=True)

    def __str__(self):
        products_str = ", ".join([product.name for product in self.products.all()])
        return f"{self.customer.user.username} - {products_str} - {self.shipping_address} - {self.purchase_date}"
