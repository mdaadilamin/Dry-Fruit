from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Sum, Count, F
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from datetime import timedelta
from apps.shop.models import Product, Category, ProductReview
from apps.orders.models import Order, CartItem, OrderItem
from apps.users.models import User, Customer
from apps.cms.models import Banner, Testimonial, HomePageHero, FooterContent, HomePageFeature
from apps.blog.models import Comment
from apps.marketing.models import Coupon

@login_required
def enhanced_admin_panel(request):
    """Enhanced admin panel dashboard"""
    if request.user.role.name != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Dashboard statistics
    total_products = Product.objects.count()
    total_customers = User.objects.filter(role__name='customer').count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Sales analytics (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    sales_data = Order.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(select={
        'day': 'date(created_at)'
    }).values('day').annotate(
        total_sales=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('day')
    
    # Top selling products
    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).filter(order_count__gt=0).order_by('-order_count')[:5]
    
    # Order status distribution
    order_status_data = Order.objects.values('order_status').annotate(
        count=Count('id')
    )
    
    # Enhanced product analytics
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lte=10, is_active=True).order_by('stock')[:5]
    
    # Best rated products (with at least 3 reviews)
    best_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        review_count__gte=3,
        is_active=True
    ).order_by('-avg_rating')[:5]
    
    # Category performance
    category_performance = Category.objects.annotate(
        product_count=Count('products'),
        total_sales=Sum('products__orderitem__quantity'),
        avg_rating=Avg('products__reviews__rating')
    ).filter(product_count__gt=0).order_by('-total_sales')
    
    # Recent product reviews
    recent_reviews = ProductReview.objects.select_related('product', 'user').order_by('-created_at')[:5]
    
    # Pending blog comments
    pending_comments = Comment.objects.filter(is_approved=False).select_related('post').order_by('-created_at')[:5]
    
    # Active coupons
    active_coupons = Coupon.objects.filter(is_active=True).order_by('-created_at')[:5]
    total_coupons = Coupon.objects.count()
    active_coupons_count = Coupon.objects.filter(is_active=True).count()
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'sales_data': list(sales_data),
        'top_products': top_products,
        'order_status_data': list(order_status_data),
        'low_stock_products': low_stock_products,
        'best_rated_products': best_rated_products,
        'category_performance': category_performance,
        'recent_reviews': recent_reviews,
        'pending_comments': pending_comments,
        'active_coupons': active_coupons,
        'total_coupons': total_coupons,
        'active_coupons_count': active_coupons_count,
    }
    return render(request, 'core/admin_panel_enhanced.html', context)

@login_required
def update_order_status(request):
    """Update order status via AJAX"""
    if request.method == 'POST' and request.user.role.name == 'admin':
        try:
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('order_status')
            
            order = get_object_or_404(Order, id=order_id)
            order.order_status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order status updated to {order.get_order_status_display()}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Failed to update order status'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    })