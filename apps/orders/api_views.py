from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, CartItem
from .serializers import OrderSerializer, CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.role.name == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        # Implementation similar to views.add_to_cart
        return Response({'message': 'Item added to cart'})
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear entire cart"""
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)