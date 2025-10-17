from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from apps.orders.models import Order, Wishlist
from .models import User, Employee, Customer, ActivityLog, Role

@login_required
def profile(request):
    """User profile management"""
    if request.method == 'POST':
        # Handle profile update
        if 'current_password' in request.POST:
            # Handle password change
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            
            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_new_password:
                messages.error(request, 'New passwords do not match.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
        else:
            # Handle profile information update
            user = request.user
            user.full_name = request.POST.get('full_name', user.full_name)
            user.email = request.POST.get('email', user.email)
            user.mobile = request.POST.get('mobile', user.mobile)
            user.save()
            
            if hasattr(user, 'customer'):
                customer = user.customer
                customer.address = request.POST.get('address', customer.address)
                customer.city = request.POST.get('city', customer.city)
                customer.pincode = request.POST.get('pincode', customer.pincode)
                customer.save()
            
            messages.success(request, 'Profile updated successfully!')
        
        return redirect('users:profile')
    
    return render(request, 'users/profile.html')

@login_required
def order_history(request):
    """View order history"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'users/order_history.html', {'orders': orders})

@login_required
def wishlist(request):
    """View wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    if request.method == 'POST':
        from apps.shop.models import Product
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        if not Wishlist.objects.filter(user=request.user, product=product).exists():
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, f'{product.name} added to your wishlist!')
        else:
            messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect('users:wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    if request.method == 'POST':
        from apps.shop.models import Product
        product = get_object_or_404(Product, id=product_id)
        
        Wishlist.objects.filter(user=request.user, product=product).delete()
        messages.success(request, f'{product.name} removed from your wishlist!')
    
    return redirect('users:wishlist')

@login_required
def employee_list(request):
    """Employee management (Admin only)"""
    if not request.user.has_permission('employees', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    employees = Employee.objects.select_related('user').all()
    return render(request, 'users/employee_list.html', {'employees': employees})

@login_required
def add_employee(request):
    """Add new employee (Admin only)"""
    if not request.user.has_permission('employees', 'add'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        status = request.POST.get('status', 'active')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate form data
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/employee_list.html', {
                'employees': Employee.objects.select_related('user').all()
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'users/employee_list.html', {
                'employees': Employee.objects.select_related('user').all()
            })
        
        # Create user
        employee_role = Role.objects.get(name='employee')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            mobile=mobile,
            role=employee_role
        )
        
        # Create employee record
        Employee.objects.create(
            user=user,
            employee_id=employee_id,
            department=department,
            status=status
        )
        
        messages.success(request, 'Employee added successfully!')
        return redirect('users:employee_list')
    
    return redirect('users:employee_list')

@login_required
def edit_employee(request, employee_id):
    """Edit employee (Admin only)"""
    if not request.user.has_permission('employees', 'edit'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        # Update employee data
        employee.user.full_name = request.POST.get('full_name', employee.user.full_name)
        employee.user.email = request.POST.get('email', employee.user.email)
        employee.user.mobile = request.POST.get('mobile', employee.user.mobile)
        employee.user.save()
        
        employee.employee_id = request.POST.get('employee_id', employee.employee_id)
        employee.department = request.POST.get('department', employee.department)
        employee.status = request.POST.get('status', employee.status)
        employee.save()
        
        messages.success(request, 'Employee updated successfully!')
        return redirect('users:employee_list')
    
    return redirect('users:employee_list')

@login_required
def customer_list(request):
    """Customer management"""
    if not request.user.has_permission('customers', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    customers = Customer.objects.select_related('user').all()
    return render(request, 'users/customer_list.html', {'customers': customers})

@login_required
def activity_log(request):
    """Activity log view"""
    if not request.user.has_permission('reports', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'users/activity_log.html', {'logs': logs})