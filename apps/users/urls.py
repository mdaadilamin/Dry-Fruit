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
    path('orders/', views.order_history, name='order_history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('customers/', views.customer_list, name='customer_list'),
    path('activity-log/', views.activity_log, name='activity_log'),
]