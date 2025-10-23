from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductVariant, ProductImage, ProductReview, GiftBoxCustomization, GiftBoxItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)} if hasattr(Category, 'slug') else {}
    
    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.products.count()

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ProductVariantInline, ProductImageInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'discount_percent')
        }),
        ('Images & Media', {
            'fields': ('image',)
        }),
        ('Additional Info', {
            'fields': ('nutritional_info', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'price', 'stock', 'is_active']
    list_filter = ['is_active', 'name', 'product__category']
    search_fields = ['product__name', 'name', 'value']
    readonly_fields = ['created_at']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['product__name', 'user__username']
    readonly_fields = ['created_at']

@admin.register(GiftBoxCustomization)
class GiftBoxCustomizationAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['product__name', 'name']
    readonly_fields = ['created_at']

@admin.register(GiftBoxItem)
class GiftBoxItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'item', 'quantity', 'is_default', 'is_removable', 'created_at']
    list_filter = ['is_default', 'is_removable', 'created_at']
    search_fields = ['product__name', 'item__name']
    readonly_fields = ['created_at']