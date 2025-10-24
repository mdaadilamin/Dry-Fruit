from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from . import views_enhanced

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('chocolates/', views.chocolates_category, name='chocolates_category'),
    path('spices/', views.spices_category, name='spices_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/enhanced/', views_enhanced.enhanced_admin_panel, name='enhanced_admin_panel'),
    path('admin-panel/coupons/', views.admin_coupon_management, name='admin_coupon_management'),
    path('admin-panel/analytics/', views.product_analytics, name='product_analytics'),
    path('admin-panel/update-order-status/', views_enhanced.update_order_status, name='update_order_status'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html',
        email_template_name='notifications/email/password_reset_email.html',
        subject_template_name='notifications/email/password_reset_subject.txt',
        success_url=reverse_lazy('core:password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]