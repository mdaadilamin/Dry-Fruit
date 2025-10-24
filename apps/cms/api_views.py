from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Banner, Testimonial
from .serializers import BannerSerializer, TestimonialSerializer

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_active_banners(request):
    """Get all active banners for popup display"""
    banners = Banner.objects.filter(
        is_active=True
    ).order_by('order', '-created_at')
    
    serializer = BannerSerializer(banners, many=True)
    return Response({
        'success': True,
        'banners': serializer.data
    })