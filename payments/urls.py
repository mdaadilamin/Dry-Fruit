from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('stripe/<int:order_id>/', views.stripe_payment, name='stripe_payment'),
    path('paypal/<int:order_id>/', views.paypal_payment, name='paypal_payment'),
    path('paypal/execute/', views.paypal_execute, name='paypal_execute'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
]