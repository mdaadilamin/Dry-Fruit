from django.contrib import admin
from .models import Banner, Testimonial, Page, ContactInfo, Newsletter

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'location', 'is_active', 'order']
    list_filter = ['rating', 'is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['customer_name', 'location']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'title', 'is_active', 'updated_at']
    list_filter = ['page_type', 'is_active']
    search_fields = ['title', 'content']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'email', 'phone']
    
    def has_add_permission(self, request):
        # Only allow one contact info instance
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']