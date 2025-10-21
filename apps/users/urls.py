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
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/reorder/<int:order_id>/', views.reorder, name='reorder'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('activity/', views.activity_log, name='activity_log'),
    path('roles/manage/', views.role_management, name='role_management'),
    path('roles/<int:role_id>/permissions/', views.update_role_permissions, name='update_role_permissions'),
]