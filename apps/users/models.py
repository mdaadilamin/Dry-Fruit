from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.get_name_display()

class Permission(models.Model):
    MODULE_CHOICES = [
        ('products', 'Products'),
        ('orders', 'Orders'),
        ('customers', 'Customers'),
        ('employees', 'Employees'),
        ('reports', 'Reports'),
        ('cms', 'Content Management'),
    ]
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['role', 'module']
    
    def __str__(self):
        return f"{self.role.name} - {self.module}"

class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username
    
    def has_permission(self, module, permission_type):
        """Check if user has specific permission for a module"""
        if not self.role:
            return False
            
        if self.role.name == 'admin':
            return True
        
        try:
            perm = Permission.objects.get(role=self.role, module=module)
            return getattr(perm, f'can_{permission_type}', False)
        except Permission.DoesNotExist:
            return False
    
    @property
    def is_admin(self):
        """Check if user is an administrator"""
        return self.role and self.role.name == 'admin'
    
    @property
    def is_employee(self):
        """Check if user is an employee"""
        return self.role and self.role.name == 'employee'
    
    @property
    def is_customer(self):
        """Check if user is a customer"""
        return self.role and self.role.name == 'customer'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, blank=True)
    hire_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ], default='active')
    
    def __str__(self):
        return f"{self.user.full_name} - {self.employee_id}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.user.full_name

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action}"