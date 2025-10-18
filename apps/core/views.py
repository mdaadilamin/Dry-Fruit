from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Sum, Count, F
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from datetime import timedelta
from apps.shop.models import Product, Category, ProductReview
from apps.orders.models import Order, CartItem
from apps.users.models import User, Customer
from apps.cms.models import Banner, Testimonial
from .utils import get_related_products, get_upsell_products, get_product_rating_stats

def home(request):
    """Home page with featured products and banners"""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    banners = Banner.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    # Get gift box products for the carousel
    try:
        gift_box_category = Category.objects.get(name='Gift Boxes')
        gift_box_products = Product.objects.filter(
            category=gift_box_category, 
            is_active=True
        )[:8]  # Limit to 8 gift box products
    except Category.DoesNotExist:
        gift_box_products = Product.objects.none()
    
    # Get featured products for each category
    category_featured_products = {}
    for category in categories:
        category_featured_products[category.name] = Product.objects.filter(
            category=category,
            is_active=True,
            is_featured=True
        )[:4]  # Limit to 4 featured products per category
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'banners': banners,
        'testimonials': testimonials,
        'gift_box_products': gift_box_products,
        'category_featured_products': category_featured_products,
    }
    return render(request, 'core/home.html', context)

def shop(request):
    """Shop page with products, filters, and search"""
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Stock filter
    in_stock_filter = request.GET.get('in_stock', '')
    if in_stock_filter:
        products = products.filter(stock__gt=0)
    
    # Sale filter
    on_sale_filter = request.GET.get('on_sale', '')
    if on_sale_filter:
        products = products.filter(discount_percent__gt=0)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popularity':
        # Order by number of reviews or featured status
        products = products.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-avg_rating', '-review_count', '-is_featured')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by('name')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_filter': in_stock_filter,
        'on_sale_filter': on_sale_filter,
        'sort_by': sort_by,
    }
    return render(request, 'core/shop.html', context)

def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get related products and upsell products using utility functions
    related_products = get_related_products(product, limit=4)
    upsell_products = get_upsell_products(product, limit=4)
    
    # Get product reviews
    reviews = ProductReview.objects.filter(product=product, is_verified=True)
    rating_stats = get_product_rating_stats(product)
    
    # Get gift box customizations and items if this is a gift box
    gift_box_customizations = None
    gift_box_items = None
    if product.category.name == 'Gift Boxes':
        gift_box_customizations = product.customizations.filter(is_active=True)
        gift_box_items = product.gift_box_items.filter(product=product)
    
    context = {
        'product': product,
        'related_products': related_products,
        'upsell_products': upsell_products,
        'reviews': reviews,
        'avg_rating': rating_stats['avg_rating'],
        'gift_box_customizations': gift_box_customizations,
        'gift_box_items': gift_box_items,
    }
    return render(request, 'core/product_detail.html', context)

@login_required
def cart(request):
    """Shopping cart page"""
    from apps.orders.models import CartItem, GiftWrap
    
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        
        if action == 'update':
            # Update quantity
            quantity = int(request.POST.get('quantity', 1))
            from apps.shop.models import Product
            product = get_object_or_404(Product, id=product_id)
            
            # Ensure quantity doesn't exceed stock
            quantity = min(quantity, product.stock)
            
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
            
            messages.success(request, f'Cart updated for {product.name}')
            
        elif action == 'remove':
            # Remove item from cart
            CartItem.objects.filter(user=request.user, product_id=product_id).delete()
            messages.success(request, 'Item removed from cart')
        
        elif action == 'apply_coupon':
            # Apply coupon code
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('marketing:apply_coupon'))
        
        elif action == 'remove_coupon':
            # Remove coupon code
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('marketing:remove_coupon'))
    
    # Get cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'product__category', 'gift_wrap')
    
    # Calculate totals
    total = sum(item.get_total_price() for item in cart_items)
    
    # Get gift wrap total
    gift_wrap_total = sum(
        (item.gift_wrap.price * item.quantity) 
        for item in cart_items 
        if item.gift_wrap
    )
    
    # Get active gift wraps
    gift_wraps = GiftWrap.objects.filter(is_active=True)
    
    # Handle coupon
    from apps.marketing.models import Coupon, CouponUsage
    coupon = None
    discount = 0
    total_with_discount = total
    
    # Check if user has an active coupon
    try:
        # Get the most recent coupon usage for this user
        coupon_usage = CouponUsage.objects.filter(
            user=request.user
        ).select_related('coupon').first()
        
        # Check if the coupon usage exists and the coupon is still valid
        if coupon_usage and coupon_usage.coupon.is_valid():
            coupon = coupon_usage.coupon
            discount = coupon.calculate_discount(total)
            total_with_discount = total - discount
    except CouponUsage.DoesNotExist:
        pass
    
    # Get related products based on items in cart
    related_products = []
    if cart_items.exists():
        # Get all products in cart
        cart_product_ids = [item.product.id for item in cart_items]
        cart_products = Product.objects.filter(id__in=cart_product_ids)
        
        # For each product in cart, get related products
        for cart_product in cart_products:
            related_for_item = get_related_products(cart_product, limit=2)
            related_products.extend(related_for_item)
        
        # Remove duplicates and limit to 6 products
        seen_ids = set()
        unique_related = []
        for product in related_products:
            if product.id not in seen_ids and product.id not in cart_product_ids:
                seen_ids.add(product.id)
                unique_related.append(product)
                if len(unique_related) >= 6:
                    break
        
        related_products = unique_related
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'gift_wrap_total': gift_wrap_total,
        'gift_wraps': gift_wraps,
        'coupon': coupon,
        'discount': discount,
        'total_with_discount': total_with_discount,
        'related_products': related_products,
    }
    return render(request, 'core/cart.html', context)

@login_required
def checkout(request):
    """Checkout page"""
    if request.method == 'POST':
        # Handle order creation
        cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'gift_wrap')
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('core:cart')
        
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')
        
        # Calculate total amount
        total_amount = sum(item.get_total_price() for item in cart_items)
        
        # Apply coupon discount if available
        if 'coupon_code' in request.session:
            from marketing.models import Coupon
            try:
                coupon = Coupon.objects.get(code=request.session['coupon_code'])
                if coupon.is_valid() and coupon.can_be_used_by_user(request.user):
                    # Calculate discount
                    if coupon.coupon_type == 'percentage':
                        discount = total_amount * (coupon.discount_value / 100)
                    elif coupon.coupon_type == 'fixed':
                        discount = min(coupon.discount_value, total_amount)
                    else:
                        discount = 0
                    
                    total_amount = total_amount - discount
                    
                    # Record coupon usage
                    from marketing.models import CouponUsage
                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=request.user
                    )
                    
                    # Update coupon usage count
                    coupon.used_count += 1
                    coupon.save()
            except Coupon.DoesNotExist:
                pass
        
        # Create order
        order = Order.objects.create(
            customer=request.user,
            total_amount=total_amount,
            payment_mode=payment_method,
            shipping_name=f"{first_name} {last_name}",
            shipping_email=email,
            shipping_mobile=phone,
            shipping_address=address,
            shipping_city=city,
            shipping_pincode=zip_code
        )
        
        # Create order items with gift wrap options
        for item in cart_items:
            from apps.orders.models import OrderItem
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                gift_wrap=item.gift_wrap  # Transfer gift wrap selection
            )
        
        # Clear cart
        cart_items.delete()
        
        # Remove coupon from session
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        
        # Send notification for new order
        from apps.notifications.services import EmailService
        from apps.notifications.models import Notification
        from django.urls import reverse
        
        # Notify customer
        if request.user.email:
            context = {
                'order_number': order.order_number,
                'customer_name': request.user.full_name,
                'order_total': order.total_amount,
                'order_date': order.created_at.strftime('%B %d, %Y'),
                'order_items': [
                    {
                        'name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.price,
                        'total': item.get_total_price()
                    }
                    for item in order.items.all()
                ],
                'shipping_address': f"{order.shipping_address}, {order.shipping_city}, {order.shipping_pincode}",
                'order_url': request.build_absolute_uri(reverse('core:dashboard'))
            }
            EmailService.send_email('order_confirmation', request.user.email, context)
        
        # Create in-app notification for customer
        Notification.objects.get_or_create(
            user=request.user,
            title=f'Order #{order.order_number} Confirmed',
            message=f'Your order #{order.order_number} for ₹{order.total_amount} has been confirmed and is being processed.',
            notification_type='success'
        )
        
        # Notify admins
        from apps.users.models import User
        admin_users = [user for user in User.objects.filter(is_active=True) if user.is_admin]
        admin_context = {
            'order_number': order.order_number,
            'customer_name': request.user.full_name,
            'order_total': order.total_amount,
            'order_date': order.created_at.strftime('%B %d, %Y'),
            'order_url': request.build_absolute_uri(reverse('orders:order_detail', args=[order.id]))
        }
        
        for admin in admin_users:
            # Create in-app notification for admins
            Notification.objects.get_or_create(
                user=admin,
                title=f'New Order #{order.order_number}',
                message=f'New order from {request.user.full_name} for ₹{order.total_amount}',
                notification_type='info'
            )
            
            # Send email notification to admins
            if admin.email:
                EmailService.send_email('order_confirmation', admin.email, admin_context)
        
        # Redirect to payment page based on selected method
        if payment_method == 'card':
            return redirect('payments:stripe_payment', order_id=order.id)
        elif payment_method == 'paypal':
            return redirect('payments:paypal_payment', order_id=order.id)
        else:
            # For Cash on Delivery, mark order as pending
            order.payment_status = 'pending'
            order.order_status = 'pending'
            order.save()
            messages.success(request, f'Order #{order.order_number} placed successfully! Payment will be collected on delivery.')
            return redirect('core:dashboard')
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'gift_wrap')
    total = sum(item.get_total_price() for item in cart_items)
    
    # Calculate gift wrap total
    gift_wrap_total = sum(
        (item.gift_wrap.price * item.quantity) 
        for item in cart_items 
        if item.gift_wrap
    )
    
    # Check for applied coupon
    coupon = None
    discount = 0
    total_with_discount = total
    
    if 'coupon_code' in request.session:
        from marketing.models import Coupon
        try:
            coupon = Coupon.objects.get(code=request.session['coupon_code'])
            if coupon.is_valid() and coupon.can_be_used_by_user(request.user):
                # Calculate discount
                if coupon.coupon_type == 'percentage':
                    discount = total * (coupon.discount_value / 100)
                elif coupon.coupon_type == 'fixed':
                    discount = min(coupon.discount_value, total)
                
                total_with_discount = total - discount
            else:
                # Remove invalid coupon
                del request.session['coupon_code']
                coupon = None
        except Coupon.DoesNotExist:
            # Remove invalid coupon code from session
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'gift_wrap_total': gift_wrap_total,
        'coupon': coupon,
        'discount': discount,
        'total_with_discount': total_with_discount,
    }
    return render(request, 'core/checkout.html', context)

@login_required
def dashboard(request):
    """Customer dashboard"""
    if request.user.role.name == 'admin':
        return redirect('core:admin_panel')
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def admin_panel(request):
    """Admin panel dashboard"""
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
    
    # Worst rated products (with at least 3 reviews)
    worst_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        review_count__gte=3,
        is_active=True
    ).order_by('avg_rating')[:5]
    
    # Products with no reviews
    products_without_reviews = Product.objects.filter(
        reviews__isnull=True,
        is_active=True
    ).order_by('name')[:5]
    
    # Category performance
    category_performance = Category.objects.annotate(
        product_count=Count('products'),
        total_sales=Sum('products__orderitem__quantity'),
        avg_rating=Avg('products__reviews__rating')
    ).filter(product_count__gt=0).order_by('-total_sales')
    
    # Recent product reviews
    recent_reviews = ProductReview.objects.select_related('product', 'user').order_by('-created_at')[:5]
    
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
        'worst_rated_products': worst_rated_products,
        'products_without_reviews': products_without_reviews,
        'category_performance': category_performance,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'core/admin_panel.html', context)

@login_required
def product_analytics(request):
    """Detailed product analytics dashboard"""
    if request.user.role.name != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Get date range filter
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Product sales over time
    sales_over_time = OrderItem.objects.filter(
        order__created_at__gte=start_date
    ).extra(select={
        'day': 'date(orders_order.created_at)'
    }).values('day').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('day')
    
    # Top selling products
    top_selling_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity'),
        total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price'))
    ).filter(total_sold__gt=0).order_by('-total_sold')[:10]
    
    # Product performance by category
    category_performance = Category.objects.annotate(
        total_products=Count('products'),
        total_sold=Sum('products__orderitem__quantity'),
        total_revenue=Sum(F('products__orderitem__quantity') * F('products__orderitem__price'))
    ).filter(total_products__gt=0).order_by('-total_sold')
    
    # Inventory analytics
    inventory_stats = {
        'total_products': Product.objects.count(),
        'out_of_stock': Product.objects.filter(stock=0).count(),
        'low_stock': Product.objects.filter(stock__lte=10, stock__gt=0).count(),
        'well_stocked': Product.objects.filter(stock__gt=10).count(),
    }
    
    # Review analytics
    review_stats = {
        'total_reviews': ProductReview.objects.count(),
        'approved_reviews': ProductReview.objects.filter(is_approved=True).count(),
        'pending_reviews': ProductReview.objects.filter(is_approved=False).count(),
        'avg_rating': ProductReview.objects.aggregate(avg=Avg('rating'))['avg'] or 0,
    }
    
    # Rating distribution
    rating_distribution = ProductReview.objects.values('rating').annotate(
        count=Count('rating')
    ).order_by('rating')
    
    context = {
        'sales_over_time': list(sales_over_time),
        'top_selling_products': top_selling_products,
        'category_performance': category_performance,
        'inventory_stats': inventory_stats,
        'review_stats': review_stats,
        'rating_distribution': list(rating_distribution),
        'days': days,
    }
    return render(request, 'core/product_analytics.html', context)

@csrf_protect
def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect admin users to admin panel, others to dashboard
            if user.is_admin:
                next_url = request.GET.get('next', 'core:admin_panel')
            else:
                next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')

def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'core/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html')
        
        # Create user
        from apps.users.models import Role
        customer_role = Role.objects.get(name='customer')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            mobile=mobile,
            role=customer_role
        )
        
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('core:login')
    
    return render(request, 'core/register.html')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

def chocolates_category(request):
    """Chocolates category page"""
    try:
        chocolates_category = Category.objects.get(name='Chocolates')
        products = Product.objects.filter(
            category=chocolates_category, 
            is_active=True
        ).select_related('category')
    except Category.DoesNotExist:
        products = Product.objects.none()
        chocolates_category = None
    
    # Apply the same filters as the general shop view
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Stock filter
    in_stock_filter = request.GET.get('in_stock', '')
    if in_stock_filter:
        products = products.filter(stock__gt=0)
    
    # Sale filter
    on_sale_filter = request.GET.get('on_sale', '')
    if on_sale_filter:
        products = products.filter(discount_percent__gt=0)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popularity':
        # Order by number of reviews or featured status
        products = products.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-avg_rating', '-review_count', '-is_featured')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by('name')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'category': chocolates_category,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_filter': in_stock_filter,
        'on_sale_filter': on_sale_filter,
        'sort_by': sort_by,
        'category_name': 'Chocolates'
    }
    return render(request, 'core/category.html', context)

def spices_category(request):
    """Spices category page"""
    try:
        spices_category = Category.objects.get(name='Spices')
        products = Product.objects.filter(
            category=spices_category, 
            is_active=True
        ).select_related('category')
    except Category.DoesNotExist:
        products = Product.objects.none()
        spices_category = None
    
    # Apply the same filters as the general shop view
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Stock filter
    in_stock_filter = request.GET.get('in_stock', '')
    if in_stock_filter:
        products = products.filter(stock__gt=0)
    
    # Sale filter
    on_sale_filter = request.GET.get('on_sale', '')
    if on_sale_filter:
        products = products.filter(discount_percent__gt=0)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popularity':
        # Order by number of reviews or featured status
        products = products.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-avg_rating', '-review_count', '-is_featured')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by('name')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'category': spices_category,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_filter': in_stock_filter,
        'on_sale_filter': on_sale_filter,
        'sort_by': sort_by,
        'category_name': 'Spices'
    }
    return render(request, 'core/category.html', context)