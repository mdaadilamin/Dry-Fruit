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
    path('manage/enquiries/', views.enquiry_management, name='enquiry_management'),
    path('manage/enquiries/<int:enquiry_id>/resolve/', views.resolve_enquiry, name='resolve_enquiry'),
    path('manage/careers/sections/', views.careers_section_management, name='careers_section_management'),
    path('manage/careers/culture/', views.careers_culture_management, name='careers_culture_management'),
    path('manage/careers/testimonials/', views.careers_testimonial_management, name='careers_testimonial_management'),
    path('manage/careers/benefits/', views.careers_benefit_management, name='careers_benefit_management'),
    path('manage/careers/openings/', views.careers_opening_management, name='careers_opening_management'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/confirm/<uuid:token>/', views.confirm_newsletter_subscription, name='confirm_newsletter'),
    path('testimonial/submit/', views.submit_testimonial, name='submit_testimonial'),
    path('enquiry/submit/', views.submit_enquiry, name='submit_enquiry'),
    path('<str:page_type>/', views.page_view, name='page_view'),
]