from rest_framework import serializers
from .models import Coupon, CouponUsage
from apps.shop.models import Category, Product

class CouponSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'coupon_type', 'discount_value', 'discount_application',
            'category', 'category_name', 'product', 'product_name',
            'max_uses', 'used_count', 'max_uses_per_user',
            'is_active', 'valid_from', 'valid_to', 'min_purchase_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['used_count', 'created_at', 'updated_at']

class CouponUsageSerializer(serializers.ModelSerializer):
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = CouponUsage
        fields = ['id', 'coupon', 'coupon_code', 'user', 'user_name', 'order', 'used_at']
        read_only_fields = ['used_at']