from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'payment_method', 'payment_status', 'amount', 'currency', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'currency', 'created_at']
    search_fields = ['order__order_number', 'user__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'user', 'payment_method', 'payment_status', 'transaction_id')
        }),
        ('Amount Details', {
            'fields': ('amount', 'currency')
        }),
        ('Payment Method Specific', {
            'fields': ('stripe_payment_intent_id', 'paypal_payment_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )