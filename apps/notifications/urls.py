from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'notifications'

# API Routes
router = DefaultRouter()
router.register(r'notifications', api_views.NotificationViewSet, basename='notification')

urlpatterns = router.urls + [
    # Web views
    path('manage/email-templates/', views.email_template_management, name='email_template_management'),
    path('manage/sms-templates/', views.sms_template_management, name='sms_template_management'),
    path('logs/email/', views.email_log, name='email_log'),
    path('logs/sms/', views.sms_log, name='sms_log'),
    # API views
    path('system-notifications/', views.get_system_notifications, name='system_notifications'),
    path('user-notifications/', views.get_user_notifications, name='user_notifications'),
]