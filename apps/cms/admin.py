from django.contrib import admin
from .models import Banner, Testimonial, Page, ContactInfo, Newsletter, Enquiry, CareersSection, CareersCultureItem, CareersTestimonial, CareersBenefit, CareersJobOpening, HomePageHero, FooterContent, HomePageFeature

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['order', 'is_active']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['customer_name', 'comment']
    list_editable = ['order', 'is_active']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'is_active', 'updated_at']
    list_filter = ['page_type', 'is_active', 'updated_at']
    search_fields = ['title', 'content']
    list_editable = ['is_active']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'email', 'phone']
    search_fields = ['business_name', 'email']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'confirmed_at']
    list_filter = ['is_active', 'subscribed_at', 'confirmed_at']
    search_fields = ['email']

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_resolved', 'created_at']
    list_filter = ['subject', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_resolved']

@admin.register(CareersSection)
class CareersSectionAdmin(admin.ModelAdmin):
    list_display = ['section_type', 'title', 'order', 'is_active', 'created_at']
    list_filter = ['section_type', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']

@admin.register(CareersCultureItem)
class CareersCultureItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']

@admin.register(CareersTestimonial)
class CareersTestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'testimonial']
    list_editable = ['order', 'is_active']

@admin.register(CareersBenefit)
class CareersBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']

@admin.register(CareersJobOpening)
class CareersJobOpeningAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'location', 'order', 'is_active', 'created_at']
    list_filter = ['department', 'location', 'is_active', 'created_at']
    search_fields = ['title', 'department', 'location', 'description']
    list_editable = ['order', 'is_active']


@admin.register(HomePageHero)
class HomePageHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'button_text', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'description']
    list_editable = ['is_active', 'order']


@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'email', 'phone', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['business_name', 'email']
    list_editable = ['is_active']


@admin.register(HomePageFeature)
class HomePageFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
