from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import User, Role, Permission, Employee, Customer, ActivityLog
from apps.orders.models import Order
from apps.shop.models import Product

@login_required
def employee_list(request):
    """List all employees"""
    if not request.user.has_permission('employees', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    employees = Employee.objects.select_related('user').all()
    return render(request, 'users/employee_list.html', {'employees': employees})

@login_required
def customer_list(request):
    """List all customers"""
    if not request.user.has_permission('customers', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    customers = Customer.objects.select_related('user').all()
    return render(request, 'users/customer_list.html', {'customers': customers})

@login_required
def profile(request):
    """User profile page"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile information
        request.user.full_name = request.POST.get('full_name', request.user.full_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.mobile = request.POST.get('mobile', request.user.mobile)
        
        customer.address = request.POST.get('address', customer.address)
        customer.city = request.POST.get('city', customer.city)
        customer.pincode = request.POST.get('pincode', customer.pincode)
        
        request.user.save()
        customer.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]
    
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)

@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'users/order_history.html', {'orders': orders})

@login_required
def reorder(request, order_id):
    """Reorder all items from a previous order"""
    # Get the order and verify it belongs to the current user
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Add all items from the order to the current user's cart
    from apps.orders.models import CartItem
    from apps.shop.models import Product
    
    added_items = 0
    failed_items = 0
    
    for item in order.items.all():
        try:
            product = item.product
            quantity = item.quantity
            
            # Check if product is still active and has sufficient stock
            if product.is_active:
                if product.stock >= quantity:
                    # Add to cart (or update quantity if already in cart)
                    cart_item, created = CartItem.objects.get_or_create(
                        user=request.user,
                        product=product,
                        defaults={'quantity': quantity}
                    )
                    
                    if not created:
                        # If item already in cart, update quantity (check stock)
                        new_quantity = cart_item.quantity + quantity
                        if product.stock >= new_quantity:
                            cart_item.quantity = new_quantity
                            cart_item.save()
                            added_items += 1
                        else:
                            # If not enough stock, add maximum available
                            max_addable = product.stock - cart_item.quantity
                            if max_addable > 0:
                                cart_item.quantity = product.stock
                                cart_item.save()
                                added_items += 1
                            else:
                                failed_items += 1
                    else:
                        added_items += 1
                else:
                    # Product exists but not enough stock
                    failed_items += 1
            else:
                # Product is not active
                failed_items += 1
        except Product.DoesNotExist:
            # Product no longer exists
            failed_items += 1
        except Exception as e:
            # Log the exception for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error reordering item {item.id}: {str(e)}")
            failed_items += 1
    
    # Provide feedback to user
    if added_items > 0 and failed_items == 0:
        messages.success(request, f'Successfully added {added_items} items to your cart!')
    elif added_items > 0 and failed_items > 0:
        messages.warning(request, f'Added {added_items} items to your cart. {failed_items} items could not be added due to stock limitations.')
    else:
        messages.error(request, 'No items could be added to your cart. Items may be out of stock or no longer available.')
    
    return redirect('users:order_history')

@login_required
def wishlist(request):
    """User wishlist"""
    # In a real implementation, you would have a Wishlist model
    # For now, we'll just show a placeholder
    return render(request, 'users/wishlist.html')

@login_required
def activity_log(request):
    """User activity log"""
    if not request.user.has_permission('reports', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:50]
    return render(request, 'users/activity_log.html', {'logs': logs})

@login_required
def role_management(request):
    """Manage roles and permissions (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # Handle role creation/update
        role_id = request.POST.get('role_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if role_id:
            # Update existing role
            role = get_object_or_404(Role, id=role_id)
            role.name = name
            role.description = description
            role.save()
            messages.success(request, f'Role "{name}" updated successfully!')
        else:
            # Create new role
            if name:
                role, created = Role.objects.get_or_create(
                    name=name,
                    defaults={'description': description}
                )
                if created:
                    messages.success(request, f'Role "{name}" created successfully!')
                else:
                    messages.warning(request, f'Role "{name}" already exists.')
            else:
                messages.error(request, 'Role name is required.')
        
        return redirect('users:role_management')
    
    roles = Role.objects.all().prefetch_related('permissions')
    modules = Permission.MODULE_CHOICES
    
    context = {
        'roles': roles,
        'modules': modules,
    }
    return render(request, 'users/role_management.html', context)

@login_required
def update_role_permissions(request, role_id):
    """Update permissions for a specific role (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        # Update permissions for this role
        for module, module_name in Permission.MODULE_CHOICES:
            # Get permission values from form
            can_view = request.POST.get(f'{module}_view') == 'on'
            can_add = request.POST.get(f'{module}_add') == 'on'
            can_edit = request.POST.get(f'{module}_edit') == 'on'
            can_delete = request.POST.get(f'{module}_delete') == 'on'
            
            # Update or create permission
            permission, created = Permission.objects.get_or_create(
                role=role,
                module=module,
                defaults={
                    'can_view': can_view,
                    'can_add': can_add,
                    'can_edit': can_edit,
                    'can_delete': can_delete,
                }
            )
            
            if not created:
                permission.can_view = can_view
                permission.can_add = can_add
                permission.can_edit = can_edit
                permission.can_delete = can_delete
                permission.save()
        
        messages.success(request, f'Permissions updated for role "{role.name}"!')
        return redirect('users:role_management')
    
    return redirect('users:role_management')