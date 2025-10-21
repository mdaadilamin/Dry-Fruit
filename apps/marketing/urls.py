from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'marketing'

# API Routes
router = DefaultRouter()
router.register(r'coupons', api_views.CouponViewSet)

urlpatterns = router.urls + [
    path('coupon/apply/', views.apply_coupon, name='apply_coupon'),
    path('coupon/apply-form/', views.apply_coupon_form, name='apply_coupon_form'),
    path('coupon/remove/', views.remove_coupon, name='remove_coupon'),
    path('coupons/', views.coupon_management, name='coupon_management'),
    path('coupon-usages/', views.coupon_usage_management, name='coupon_usage_management'),
    path('coupon-usages/delete/<int:usage_id>/', views.delete_coupon_usage, name='delete_coupon_usage'),
]