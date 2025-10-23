from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Coupon, CouponUsage
from apps.orders.models import Order, CartItem
from apps.shop.models import Category, Product
import json

@require_POST
def apply_coupon(request):
    """Apply coupon to cart"""
    try:
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')
        user = request.user
        
        if not coupon_code:
            return JsonResponse({
                'success': False,
                'message': 'Coupon code is required'
            })
        
        coupon = get_object_or_404(Coupon, code=coupon_code)
        
        # Check if coupon is valid
        if not coupon.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'This coupon is not valid'
            })
        
        # Check if user can use this coupon
        if not coupon.can_be_used_by_user(user):
            return JsonResponse({
                'success': False,
                'message': 'You cannot use this coupon'
            })
        
        # Store coupon in session for later use during checkout
        request.session['coupon_code'] = coupon_code
        
        return JsonResponse({
            'success': True,
            'message': f'Coupon "{coupon_code}" applied successfully!',
            'coupon': {
                'code': coupon.code,
                'type': coupon.coupon_type,
                'value': str(coupon.discount_value)
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid coupon code or an error occurred'
        })

@require_POST
def apply_coupon_form(request):
    """Apply coupon to cart via form submission"""
    coupon_code = request.POST.get('coupon_code')
    
    if not coupon_code:
        messages.error(request, 'Coupon code is required')
        return redirect('core:cart')
    
    try:
        coupon = get_object_or_404(Coupon, code=coupon_code)
        
        # Check if coupon is valid
        if not coupon.is_valid():
            messages.error(request, 'This coupon is not valid')
            return redirect('core:cart')
        
        # Check if user can use this coupon
        if not coupon.can_be_used_by_user(request.user):
            messages.error(request, 'You cannot use this coupon')
            return redirect('core:cart')
        
        # Store coupon in session for later use during checkout
        request.session['coupon_code'] = coupon_code
        messages.success(request, f'Coupon "{coupon_code}" applied successfully!')
        
    except Exception as e:
        messages.error(request, 'Invalid coupon code or an error occurred')
    
    return redirect('core:cart')

def remove_coupon(request):
    """Remove coupon from session"""
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        messages.success(request, 'Coupon removed successfully!')
    return redirect('core:cart')

def calculate_discount(coupon, cart_items, cart_total):
    """Calculate discount amount based on coupon and cart"""
    if not coupon or not coupon.is_valid():
        return 0.0
    
    # Check minimum purchase requirement
    if coupon.min_purchase_amount and cart_total < float(coupon.min_purchase_amount):
        return 0.0
    
    # Apply discount based on coupon type
    if coupon.coupon_type == 'percentage':
        return float(cart_total) * (float(coupon.discount_value) / 100.0)
    elif coupon.coupon_type == 'fixed':
        return min(float(coupon.discount_value), float(cart_total))
    elif coupon.coupon_type == 'free_shipping':
        # For free shipping, we would need shipping cost calculation
        # For now, we'll return 0 as we don't have shipping costs in the cart
        return 0.0
    
    return 0.0

@login_required
def coupon_management(request):
    """Coupon management page (Admin only)"""
    if not request.user.has_permission('products', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # Handle coupon creation/update
        coupon_id = request.POST.get('coupon_id')
        
        if coupon_id:
            # Update existing coupon
            coupon = get_object_or_404(Coupon, id=coupon_id)
            if not request.user.has_permission('products', 'edit'):
                messages.error(request, 'Access denied.')
                return redirect('marketing:coupon_management')
        else:
            # Create new coupon
            if not request.user.has_permission('products', 'add'):
                messages.error(request, 'Access denied.')
                return redirect('marketing:coupon_management')
            coupon = Coupon()
        
        # Update coupon fields
        coupon.code = request.POST.get('code', '')
        coupon.coupon_type = request.POST.get('coupon_type', 'percentage')
        coupon.discount_value = request.POST.get('discount_value', 0)
        coupon.discount_application = request.POST.get('discount_application', 'cart')
        
        category_id = request.POST.get('category')
        if category_id:
            try:
                coupon.category_id = int(category_id)
            except (ValueError, TypeError):
                coupon.category_id = None
        else:
            coupon.category_id = None
            
        product_id = request.POST.get('product')
        if product_id:
            try:
                coupon.product_id = int(product_id)
            except (ValueError, TypeError):
                coupon.product_id = None
        else:
            coupon.product_id = None
            
        max_uses = request.POST.get('max_uses')
        if max_uses:
            try:
                coupon.max_uses = int(max_uses)
            except (ValueError, TypeError):
                coupon.max_uses = None
        else:
            coupon.max_uses = None
        
        try:
            coupon.max_uses_per_user = int(request.POST.get('max_uses_per_user', 1))
        except (ValueError, TypeError):
            coupon.max_uses_per_user = 1
        
        min_purchase = request.POST.get('min_purchase_amount')
        if min_purchase:
            try:
                coupon.min_purchase_amount = float(min_purchase)
            except (ValueError, TypeError):
                coupon.min_purchase_amount = None
        else:
            coupon.min_purchase_amount = None
        
        valid_to = request.POST.get('valid_to')
        if valid_to:
            try:
                from datetime import datetime
                coupon.valid_to = datetime.strptime(valid_to, '%Y-%m-%d')
            except (ValueError, TypeError):
                coupon.valid_to = None
        else:
            coupon.valid_to = None
        
        coupon.is_active = 'is_active' in request.POST
        
        coupon.save()
        messages.success(request, f'Coupon {"updated" if coupon_id else "created"} successfully!')
        return redirect('marketing:coupon_management')
    
    # Display coupons
    coupons = Coupon.objects.all()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(coupons, 20)  # Show 20 coupons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    context = {
        'coupons': page_obj,
        'categories': categories,
        'products': products,
        'can_add': request.user.has_permission('products', 'add'),
        'can_edit': request.user.has_permission('products', 'edit'),
        'can_delete': request.user.has_permission('products', 'delete'),
    }
    return render(request, 'marketing/coupon_management.html', context)

@login_required
def coupon_usage_management(request):
    """Coupon usage management page (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Get filters
    search_query = request.GET.get('search', '')
    coupon_filter = request.GET.get('coupon', '')
    user_filter = request.GET.get('user', '')
    
    # Get all coupon usages with filtering
    coupon_usages = CouponUsage.objects.select_related('coupon', 'user', 'order').order_by('-used_at')
    
    if search_query:
        coupon_usages = coupon_usages.filter(
            Q(coupon__code__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__full_name__icontains=search_query)
        )
    
    if coupon_filter:
        coupon_usages = coupon_usages.filter(coupon_id=coupon_filter)
    
    if user_filter:
        coupon_usages = coupon_usages.filter(user__username__icontains=user_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(coupon_usages, 20)  # Show 20 usages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all coupons for filter dropdown
    coupons = Coupon.objects.all()
    
    context = {
        'coupon_usages': page_obj,
        'page_obj': page_obj,
        'coupons': coupons,
        'search_query': search_query,
        'coupon_filter': coupon_filter,
        'user_filter': user_filter,
    }
    return render(request, 'marketing/coupon_usage_management.html', context)

@login_required
def delete_coupon_usage(request, usage_id):
    """Delete a coupon usage record"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    usage = get_object_or_404(CouponUsage, id=usage_id)
    
    if request.method == 'POST':
        # Decrement the coupon's used count
        usage.coupon.used_count = max(0, usage.coupon.used_count - 1)
        usage.coupon.save()
        
        # Delete the usage record
        usage.delete()
        
        messages.success(request, 'Coupon usage record deleted successfully!')
        return redirect('marketing:coupon_usage_management')
    
    context = {
        'usage': usage,
    }
    return render(request, 'marketing/coupon_usage_confirm_delete.html', context)
