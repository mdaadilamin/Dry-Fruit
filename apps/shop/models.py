from django.db import models
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    nutritional_info = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    
    # Marketing fields
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for marketing")
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('core:product_detail', args=[self.id])
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    @property
    def is_low_stock(self):
        return self.stock <= 10
    
    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price
    
    @property
    def has_discount(self):
        return self.discount_percent > 0

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text="e.g., Size, Weight, Color")
    value = models.CharField(max_length=100, help_text="e.g., 250g, 500g, Large")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for this variant (overrides product price if set)")
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['product', 'name', 'value']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    @property
    def is_low_stock(self):
        return self.stock <= 5

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.product.name} - Image"

class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # For moderation
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.rating} stars"

class GiftBoxCustomization(models.Model):
    """Model for gift box customizations"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customizations')
    name = models.CharField(max_length=100, help_text="Name of the customization option (e.g., 'Add Message Card')")
    description = models.TextField(blank=True, help_text="Description of the customization option")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, 
                               help_text="Additional price for this customization")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"

class GiftBoxItem(models.Model):
    """Model for items that can be included in a gift box"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gift_box_items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='included_in_boxes')
    quantity = models.PositiveIntegerField(default=1)
    is_default = models.BooleanField(default=False, help_text="Is this item included by default?")
    is_removable = models.BooleanField(default=True, help_text="Can this item be removed from the box?")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['product', 'item']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.product.name} includes {self.item.name}"