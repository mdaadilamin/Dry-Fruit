from django.db import models
from django.utils import timezone
import uuid

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
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return str(self.title)

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
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ]
    
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
        ('careers', 'Careers'),  # Added careers page
    ]
    
    page_type = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['page_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return str(self.title)

class ContactInfo(models.Model):
    business_name = models.CharField(max_length=100, default='DRY FRUITS DELIGHT')
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
        return str(self.business_name)
    
    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # Changed to False by default for email confirmation
    confirmation_token = models.UUIDField(default=uuid.uuid4)
    subscribed_at = models.DateTimeField(default=timezone.now)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['subscribed_at']),
            models.Index(fields=['confirmation_token']),
        ]
    
    def __str__(self):
        return str(self.email)
    
    def confirm_subscription(self):
        """Confirm the newsletter subscription"""
        self.is_active = True
        self.confirmed_at = timezone.now()
        self.save()

class Enquiry(models.Model):
    """Model for customer enquiries"""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('order', 'Order Support'),
        ('product', 'Product Information'),
        ('wholesale', 'Wholesale Inquiry'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['subject']),
            models.Index(fields=['is_resolved']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Enquiry from {self.name} - {self.subject}"
    
    def resolve(self):
        """Mark enquiry as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()

class CareersSection(models.Model):
    """Model for dynamic content sections on the Careers page"""
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('culture', 'Culture Section'),
        ('testimonials', 'Testimonials Section'),
        ('benefits', 'Benefits Section'),
        ('openings', 'Job Openings Section'),
        ('cta', 'Call to Action Section'),
    ]
    
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'section_type']
        indexes = [
            models.Index(fields=['section_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.get_section_type_display()}: {self.title}"

class CareersCultureItem(models.Model):
    """Model for culture items in the Careers page"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name (e.g., 'heart', 'users')")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.title

class CareersTestimonial(models.Model):
    """Model for employee testimonials on the Careers page"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    testimonial = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class CareersBenefit(models.Model):
    """Model for employee benefits on the Careers page"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name (e.g., 'heart-pulse', 'calendar')")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.title

class CareersJobOpening(models.Model):
    """Model for job openings on the Careers page"""
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return self.title


class HomePageHero(models.Model):
    """Model for managing homepage hero section content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=200)  # Can be URL name or actual URL
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Homepage Hero"
        verbose_name_plural = "Homepage Heroes"
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.title


class FooterContent(models.Model):
    """Model for managing footer content"""
    business_name = models.CharField(max_length=100, default="DRY FRUITS DELIGHT")
    copyright_text = models.CharField(max_length=200, default="© 2024 DRY FRUITS DELIGHT. All rights reserved.")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Footer Content"
        verbose_name_plural = "Footer Content"
    
    def __str__(self):
        return f"Footer Content for {self.business_name}"


class HomePageFeature(models.Model):
    """Model for managing homepage features/why choose us section"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name (e.g., 'leaf', 'award')")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Homepage Feature"
        verbose_name_plural = "Homepage Features"
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.title
