from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Coupon, CouponUsage
from .serializers import CouponSerializer
from apps.shop.models import Category, Product

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        """Apply coupon to user's cart"""
        coupon_code = request.data.get('coupon_code')
        
        if not coupon_code:
            return Response({
                'success': False,
                'message': 'Coupon code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
            # Check if coupon is valid
            if not coupon.is_valid():
                return Response({
                    'success': False,
                    'message': 'This coupon is not valid'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user can use this coupon
            if not coupon.can_be_used_by_user(request.user):
                return Response({
                    'success': False,
                    'message': 'You cannot use this coupon'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(coupon)
            return Response({
                'success': True,
                'message': f'Coupon "{coupon_code}" applied successfully!',
                'coupon': serializer.data
            })
            
        except Coupon.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid coupon code'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def remove_coupon(self, request):
        """Remove coupon from user's session"""
        # In a real implementation, you would remove the coupon from the user's session
        return Response({
            'success': True,
            'message': 'Coupon removed successfully!'
        })