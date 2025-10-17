from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'cms'

# API Routes
router = DefaultRouter()
router.register(r'banners', api_views.BannerViewSet)
router.register(r'testimonials', api_views.TestimonialViewSet)

urlpatterns = router.urls + [
    # Web views
    path('manage/banners/', views.banner_management, name='banner_management'),
    path('manage/testimonials/', views.testimonial_management, name='testimonial_management'),
    path('manage/pages/', views.page_management, name='page_management'),
    path('manage/contact/', views.contact_management, name='contact_management'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('<str:page_type>/', views.page_view, name='page_view'),
]