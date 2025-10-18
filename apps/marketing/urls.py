from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'marketing'

# API Routes
router = DefaultRouter()
router.register(r'coupons', api_views.CouponViewSet)

urlpatterns = router.urls + [
    path('coupon/apply/', views.apply_coupon, name='apply_coupon'),
    path('coupon/remove/', views.remove_coupon, name='remove_coupon'),
    path('coupons/', views.coupon_management, name='coupon_management'),
]