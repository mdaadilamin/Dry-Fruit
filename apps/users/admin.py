from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Permission, Employee, Customer, ActivityLog

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'module', 'can_add', 'can_edit', 'can_delete', 'can_view']
    list_filter = ['role', 'module']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'full_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'full_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('full_name', 'mobile', 'role')}),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'status', 'hire_date']
    list_filter = ['status', 'department']
    search_fields = ['user__full_name', 'employee_id']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'total_orders', 'total_spent']
    search_fields = ['user__full_name', 'city']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'module', 'timestamp']
    list_filter = ['module', 'timestamp']
    search_fields = ['user__username', 'action']
    readonly_fields = ['timestamp']