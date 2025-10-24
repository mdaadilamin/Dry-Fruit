from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'notifications'

# API Routes
router = DefaultRouter()
router.register(r'notifications', api_views.NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('system-notifications/', views.system_notification_management, name='system_notification_management'),
    path('user-notifications/', views.get_user_notifications, name='get_user_notifications'),
    path('check-low-stock/', views.check_low_stock_view, name='check_low_stock'),
]