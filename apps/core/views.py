from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from apps.shop.models import Product, Category
from apps.orders.models import Order, CartItem
from apps.users.models import User
from apps.cms.models import Banner, Testimonial

def home(request):
    """Home page with featured products and banners"""
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]
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
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
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
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'min_price': min_price,
        'max_price': max_price,
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
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'core/product_detail.html', context)

@login_required
def cart(request):
    """Shopping cart page"""
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'core/cart.html', context)

@login_required
def checkout(request):
    """Checkout page"""
    if request.method == 'POST':
        # Handle order creation
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('core:cart')
        
        # Create order logic here
        messages.success(request, 'Order placed successfully!')
        return redirect('core:dashboard')
    
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
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
    total_revenue = sum(order.total_amount for order in Order.objects.all())
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
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