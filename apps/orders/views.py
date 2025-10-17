from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Order, OrderItem, CartItem
from apps.shop.models import Product
import json

@login_required
def order_management(request):
    """Order management page (Admin/Employee only)"""
    if not request.user.has_permission('orders', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    orders = Order.objects.select_related('customer').prefetch_related('items__product')
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    
    customer_filter = request.GET.get('customer')
    if customer_filter:
        orders = orders.filter(customer__full_name__icontains=customer_filter)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status_filter,
        'customer_filter': customer_filter,
        'can_edit': request.user.has_permission('orders', 'edit'),
    }
    return render(request, 'orders/order_management.html', context)

@login_required
def order_detail(request, order_id):
    """Order detail and status update"""
    if not request.user.has_permission('orders', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST' and request.user.has_permission('orders', 'edit'):
        new_status = request.POST.get('order_status')
        if new_status and new_status != order.order_status:
            order.order_status = new_status
            order.save()
            
            # Here you would trigger email notifications
            messages.success(request, f'Order status updated to {order.get_order_status_display()}')
    
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        if product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': 'Insufficient stock available'
            })
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock available'
                })
            cart_item.save()
        
        # Get updated cart count
        cart_count = CartItem.objects.filter(user=request.user).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart successfully',
            'cart_count': cart_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while adding to cart'
        })

@login_required
@require_POST
def update_cart(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        quantity = data.get('quantity')
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart'
            })
        
        if cart_item.product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': 'Insufficient stock available'
            })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated successfully',
            'new_total': float(cart_item.get_total_price())
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while updating cart'
        })

@login_required
@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while removing item'
        })