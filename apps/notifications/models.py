from django.db import models
from django.utils import timezone
from apps.users.models import User

class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('order_confirmation', 'Order Confirmation'),
        ('order_shipped', 'Order Shipped'),
        ('order_delivered', 'Order Delivered'),
        ('welcome', 'Welcome Email'),
        ('password_reset', 'Password Reset'),
    ]
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, unique=True)
    subject = models.CharField(max_length=200)
    body_html = models.TextField()
    body_text = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['template_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_template_type_display()} - {self.subject}"

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    template_type = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['recipient']),
            models.Index(fields=['template_type']),
        ]
    
    def __str__(self):
        return f"{self.recipient} - {self.subject} - {self.status}"

class SMSTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('order_confirmation', 'Order Confirmation'),
        ('order_shipped', 'Order Shipped'),
        ('order_delivered', 'Order Delivered'),
        ('welcome', 'Welcome SMS'),
        ('otp', 'OTP Verification'),
    ]
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, unique=True)
    message = models.TextField(max_length=160)  # SMS character limit
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['template_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_template_type_display()} SMS"

class SMSLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    recipient = models.CharField(max_length=15)
    message = models.TextField()
    template_type = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['recipient']),
            models.Index(fields=['template_type']),
        ]
    
    def __str__(self):
        return f"{self.recipient} - {self.template_type} - {self.status}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SystemNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('promotion', 'Promotion'),
        ('new_arrival', 'New Arrival'),
        ('announcement', 'Announcement'),
        ('alert', 'Alert'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='announcement')
    is_active = models.BooleanField(default=True)
    show_to_users = models.BooleanField(default=True)  # Whether to show to logged-in users
    show_to_guests = models.BooleanField(default=True)  # Whether to show to guests
    created_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)  # Optional expiration date
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['valid_until']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.notification_type})"
    
    def is_valid(self):
        """Check if notification is still valid"""
        if not self.is_active:
            return False
        
        if self.valid_until and timezone.now() > self.valid_until:
            return False
            
        return True