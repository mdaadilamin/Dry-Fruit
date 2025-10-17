from rest_framework import serializers
from .models import Order, OrderItem, CartItem
from apps.shop.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'get_total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'total_amount',
            'payment_mode', 'payment_status', 'order_status', 'shipping_name',
            'shipping_email', 'shipping_mobile', 'shipping_address',
            'shipping_city', 'shipping_pincode', 'created_at', 'items'
        ]
        read_only_fields = ['order_number', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price', 'created_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()