# import stripe
# import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from apps.orders.models import Order
from .models import Payment

# Stripe configuration
# stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

# PayPal configuration
# paypalrestsdk.configure({
#     'mode': getattr(settings, 'PAYPAL_MODE', 'sandbox'),  # sandbox or live
#     'client_id': getattr(settings, 'PAYPAL_CLIENT_ID', ''),
#     'client_secret': getattr(settings, 'PAYPAL_CLIENT_SECRET', '')
# })

@login_required
def stripe_payment(request, order_id):
    """Process Stripe payment"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if request.method == 'POST':
        try:
            # Create a PaymentIntent with the order amount
            # intent = stripe.PaymentIntent.create(
            #     amount=int(order.total_amount * 100),  # Stripe expects amount in cents
            #     currency='usd',
            #     metadata={
            #         'order_id': order.id,
            #         'user_id': request.user.id
            #     }
            # )
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                user=request.user,
                payment_method='stripe',
                amount=order.total_amount,
                # transaction_id=intent.id,
                # stripe_payment_intent_id=intent.id
            )
            
            return JsonResponse({
                # 'client_secret': intent.client_secret
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # For GET request, render the payment page
    context = {
        'order': order,
        # 'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', '')
    }
    return render(request, 'payments/stripe_payment.html', context)

@login_required
def paypal_payment(request, order_id):
    """Process PayPal payment"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if request.method == 'POST':
        try:
            # Create PayPal payment
            # payment = paypalrestsdk.Payment({
            #     "intent": "sale",
            #     "payer": {
            #         "payment_method": "paypal"
            #     },
            #     "redirect_urls": {
            #         "return_url": request.build_absolute_uri(
            #             reverse('payments:paypal_execute')
            #         ),
            #         "cancel_url": request.build_absolute_uri(
            #             reverse('payments:paypal_cancel')
            #         )
            #     },
            #     "transactions": [{
            #         "item_list": {
            #             "items": [{
            #                 "name": f"Order #{order.order_number}",
            #                 "sku": str(order.id),
            #                 "price": str(order.total_amount),
            #                 "currency": "USD",
            #                 "quantity": 1
            #             }]
            #         },
            #         "amount": {
            #             "total": str(order.total_amount),
            #             "currency": "USD"
            #         },
            #         "description": f"Payment for Order #{order.order_number}"
            #     }]
            # })
            
            # if payment.create():
                # Create payment record
                Payment.objects.create(
                    order=order,
                    user=request.user,
                    payment_method='paypal',
                    amount=order.total_amount,
                    # paypal_payment_id=payment.id
                )
                
                # Redirect to PayPal for approval
                # for link in payment.links:
                #     if link.rel == "approval_url":
                #         approval_url = str(link.href)
                #         return JsonResponse({'approval_url': approval_url})
            # else:
            #     return JsonResponse({'error': payment.error}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    context = {
        'order': order
    }
    return render(request, 'payments/paypal_payment.html', context)

@login_required
def paypal_execute(request):
    """Execute PayPal payment after user approval"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    if not payment_id or not payer_id:
        messages.error(request, 'Invalid PayPal payment parameters.')
        return redirect('core:dashboard')
    
    try:
        # payment = paypalrestsdk.Payment.find(payment_id)
        
        # if payment.execute({"payer_id": payer_id}):
            # Update payment status
            # payment_record = Payment.objects.get(paypal_payment_id=payment_id)
            # payment_record.payment_status = 'completed'
            # payment_record.transaction_id = payment_id
            # payment_record.save()
            
            # Update order status
            # payment_record.order.payment_status = 'paid'
            # payment_record.order.order_status = 'processing'
            # payment_record.order.save()
            
            messages.success(request, 'Payment completed successfully!')
            return redirect('core:dashboard')
        # else:
            # Update payment status to failed
            # payment_record = Payment.objects.get(paypal_payment_id=payment_id)
            # payment_record.payment_status = 'failed'
            # payment_record.save()
            
            # messages.error(request, 'Payment failed. Please try again.')
            # return redirect('core:dashboard')
            
    except Exception as e:
        messages.error(request, f'Payment execution failed: {str(e)}')
        return redirect('core:dashboard')

def paypal_cancel(request):
    """Handle PayPal payment cancellation"""
    messages.info(request, 'Payment was cancelled.')
    return redirect('core:dashboard')