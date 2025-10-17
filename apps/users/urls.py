from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'users'

# API Routes
router = DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'roles', api_views.RoleViewSet)
router.register(r'permissions', api_views.PermissionViewSet)

urlpatterns = router.urls + [
    # Web views
    path('profile/', views.profile, name='profile'),
    path('employees/', views.employee_list, name='employee_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('activity-log/', views.activity_log, name='activity_log'),
]