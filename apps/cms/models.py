from django.db import models
from django.utils import timezone

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"

class Page(models.Model):
    PAGE_CHOICES = [
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
        ('privacy', 'Privacy Policy'),
        ('terms', 'Terms & Conditions'),
        ('shipping', 'Shipping Policy'),
        ('returns', 'Returns & Refunds'),
    ]
    
    page_type = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ContactInfo(models.Model):
    business_name = models.CharField(max_length=100, default='NutriHarvest')
    tagline = models.CharField(max_length=200, default='Premium Dry Fruits & Nuts')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Business Hours
    business_hours = models.TextField(blank=True)
    
    def __str__(self):
        return self.business_name
    
    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']