from django.db import models
from django.utils import timezone
from apps.shop.models import Category, Product
from apps.users.models import User

class Coupon(models.Model):
    COUPON_TYPES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    DISCOUNT_APPLICATION = [
        ('cart', 'Entire Cart'),
        ('category', 'Specific Category'),
        ('product', 'Specific Product'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_application = models.CharField(max_length=20, choices=DISCOUNT_APPLICATION, default='cart')
    
    # Optional filters
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    
    # Usage limits
    max_uses = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of times this coupon can be used (leave blank for unlimited)")
    used_count = models.PositiveIntegerField(default=0)
    max_uses_per_user = models.PositiveIntegerField(default=1, help_text="Maximum number of times a single user can use this coupon")
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    # Minimum purchase requirement
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                            help_text="Minimum cart amount required to use this coupon")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.get_coupon_type_display()}"
    
    def is_valid(self):
        """Check if coupon is currently valid"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False
            
        if self.valid_to and now > self.valid_to:
            return False
            
        if self.max_uses and self.used_count >= self.max_uses:
            return False
            
        return True
    
    def can_be_used_by_user(self, user):
        """Check if user can use this coupon"""
        if not self.is_valid():
            return False
            
        # Check user usage limit
        user_usage_count = CouponUsage.objects.filter(coupon=self, user=user).count()
        if user_usage_count >= self.max_uses_per_user:
            return False
            
        return True

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    used_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-used_at']
        unique_together = ['coupon', 'user', 'order']
    
    def __str__(self):
        return f"{self.coupon.code} used by {self.user.username}"