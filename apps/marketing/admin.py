from django.contrib import admin
from .models import Coupon, CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'discount_value', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['coupon_type', 'is_active', 'discount_application', 'valid_from', 'valid_to']
    search_fields = ['code']
    readonly_fields = ['used_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'coupon_type', 'discount_value', 'discount_application')
        }),
        ('Targeting', {
            'fields': ('category', 'product'),
            'classes': ('collapse',)
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'used_count', 'max_uses_per_user')
        }),
        ('Validity Period', {
            'fields': ('is_active', 'valid_from', 'valid_to')
        }),
        ('Minimum Purchase', {
            'fields': ('min_purchase_amount',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'order', 'used_at']
    list_filter = ['used_at', 'coupon']
    search_fields = ['coupon__code', 'user__username']
    readonly_fields = ['used_at']