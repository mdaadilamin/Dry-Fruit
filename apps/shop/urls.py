from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'shop'

# API Routes
router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'categories', api_views.CategoryViewSet)

urlpatterns = router.urls + [
    # Web views
    path('manage/products/', views.product_management, name='product_management'),
    path('manage/categories/', views.category_management, name='category_management'),
    path('manage/products/add/', views.product_add, name='product_add'),
    path('manage/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('manage/reviews/', views.review_management, name='review_management'),
]