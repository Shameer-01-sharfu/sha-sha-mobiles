from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Apple', 'Apple'),
        ('Samsung', 'Samsung'),
        ('Vivo', 'Vivo'),
        ('Oppo', 'Oppo'),
        ('Realme', 'Realme'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Other'
    )

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)

    image = CloudinaryField(
        'image',
        blank=True,
        null=True
    )
    
  
    def __str__(self):
        return self.name


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()

    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=100,
        default="Cash on Delivery"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderHistory(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History #{self.id} - {self.product_name}"