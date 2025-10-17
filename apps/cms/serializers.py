from rest_framework import serializers
from .models import Banner, Testimonial, Page, ContactInfo

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'description', 'image', 'button_text', 'button_link', 'order']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'customer_name', 'customer_image', 'rating', 'comment', 'location']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['page_type', 'title', 'content', 'meta_description']

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'