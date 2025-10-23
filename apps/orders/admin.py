from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, CartItem, Wishlist, GiftWrap

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price', 'get_total_price']
    extra = 0
    
    @admin.display(description='Total Price')
    def get_total_price(self, obj):
        return obj.get_total_price()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'total_amount', 'payment_mode', 'order_status', 'created_at']
    list_filter = ['order_status', 'payment_mode', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer__full_name', 'shipping_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'total_amount')
        }),
        ('Payment & Status', {
            'fields': ('payment_mode', 'payment_status', 'order_status')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_mobile', 
                      'shipping_address', 'shipping_city', 'shipping_pincode')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    
    @admin.display(description='Total Price')
    def get_total_price(self, obj):
        return obj.get_total_price()

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(GiftWrap)
class GiftWrapAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']