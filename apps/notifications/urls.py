from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('system-notifications/', views.system_notification_management, name='system_notification_management'),
    path('check-low-stock/', views.check_low_stock_view, name='check_low_stock'),  # Add this line
]
