from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'orders'

# API Routes
router = DefaultRouter()
router.register(r'orders', api_views.OrderViewSet, basename='orders')
router.register(r'cart', api_views.CartItemViewSet, basename='cart')

urlpatterns = router.urls + [
    # Web views
    path('manage/', views.order_management, name='order_management'),
    path('manage/<int:order_id>/', views.order_detail, name='order_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update-gift-wrap/', views.update_gift_wrap, name='update_gift_wrap'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    # API endpoints
    path('api/wishlist-count/', api_views.wishlist_count, name='wishlist_count'),
]