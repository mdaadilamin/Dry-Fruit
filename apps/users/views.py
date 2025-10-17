from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Employee, Customer, ActivityLog

@login_required
def profile(request):
    """User profile management"""
    if request.method == 'POST':
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
    
    return render(request, 'users/profile.html')

@login_required
def employee_list(request):
    """Employee management (Admin only)"""
    if not request.user.has_permission('employees', 'view'):
        messages.error(request, 'Access denied.')
        return render(request, 'core/dashboard.html')
    
    employees = Employee.objects.select_related('user').all()
    return render(request, 'users/employee_list.html', {'employees': employees})

@login_required
def customer_list(request):
    """Customer management"""
    if not request.user.has_permission('customers', 'view'):
        messages.error(request, 'Access denied.')
        return render(request, 'core/dashboard.html')
    
    customers = Customer.objects.select_related('user').all()
    return render(request, 'users/customer_list.html', {'customers': customers})

@login_required
def activity_log(request):
    """Activity log view"""
    if not request.user.has_permission('reports', 'view'):
        messages.error(request, 'Access denied.')
        return render(request, 'core/dashboard.html')
    
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'users/activity_log.html', {'logs': logs})