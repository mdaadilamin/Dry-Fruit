from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.shop.models import Product, Category, ProductReview
from apps.orders.models import Order, CartItem
from apps.users.models import User, Customer
from apps.cms.models import Banner, Testimonial

def home(request):
    """Home page with featured products and banners"""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    banners = Banner.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'banners': banners,
        'testimonials': testimonials,
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
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product_id)[:4]
    
    # Get product reviews
    reviews = ProductReview.objects.filter(product=product, is_verified=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'core/product_detail.html', context)

@login_required
def cart(request):
    """Shopping cart page"""
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
            coupon_code = request.POST.get('coupon_code')
            # Redirect to the marketing app's apply coupon view
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('marketing:apply_coupon'))
        
        elif action == 'remove_coupon':
            # Remove coupon code
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('marketing:remove_coupon'))
        
        return redirect('core:cart')
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.get_total_price() for item in cart_items)
    
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
        'coupon': coupon,
        'discount': discount,
        'total_with_discount': total_with_discount,
    }
    return render(request, 'core/cart.html', context)

@login_required
def checkout(request):
    """Checkout page"""
    if request.method == 'POST':
        # Handle order creation
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
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
        
        # Create order items
        for item in cart_items:
            from apps.orders.models import OrderItem
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear cart
        cart_items.delete()
        
        # Remove coupon from session
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        
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
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.get_total_price() for item in cart_items)
    
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
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'sales_data': list(sales_data),
        'top_products': top_products,
        'order_status_data': list(order_status_data),
    }
    return render(request, 'core/admin_panel.html', context)

def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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