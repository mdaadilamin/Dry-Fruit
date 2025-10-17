from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.shop.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'product']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"
    
    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Shipping Information
    shipping_name = models.CharField(max_length=100)
    shipping_email = models.EmailField()
    shipping_mobile = models.CharField(max_length=15)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50)
    shipping_pincode = models.CharField(max_length=10)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['customer']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = 'NH' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'product']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"