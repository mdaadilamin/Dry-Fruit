from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Category

@login_required
def product_management(request):
    """Product management page (Admin/Employee only)"""
    if not request.user.has_permission('products', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    products = Product.objects.select_related('category').all()
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'can_add': request.user.has_permission('products', 'add'),
        'can_edit': request.user.has_permission('products', 'edit'),
        'can_delete': request.user.has_permission('products', 'delete'),
    }
    return render(request, 'shop/product_management.html', context)

@login_required
def category_management(request):
    """Category management page"""
    if not request.user.has_permission('products', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('products', 'add'):
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Category name is required.')
    
    categories = Category.objects.all()
    return render(request, 'shop/category_management.html', {'categories': categories})

@login_required
def product_add(request):
    """Add new product"""
    if not request.user.has_permission('products', 'add'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        nutritional_info = request.POST.get('nutritional_info', '')
        image = request.FILES.get('image')
        
        if all([name, category_id, price, stock, description]):
            try:
                category = Category.objects.get(id=category_id)
                Product.objects.create(
                    name=name,
                    category=category,
                    price=price,
                    stock=stock,
                    description=description,
                    nutritional_info=nutritional_info,
                    image=image
                )
                messages.success(request, 'Product added successfully!')
                return redirect('shop:product_management')
            except Category.DoesNotExist:
                messages.error(request, 'Invalid category selected.')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    categories = Category.objects.filter(is_active=True)
    return render(request, 'shop/product_add.html', {'categories': categories})

@login_required
def product_edit(request, product_id):
    """Edit existing product"""
    if not request.user.has_permission('products', 'edit'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        category_id = request.POST.get('category')
        if category_id:
            try:
                product.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)
        product.description = request.POST.get('description', product.description)
        product.nutritional_info = request.POST.get('nutritional_info', product.nutritional_info)
        
        image = request.FILES.get('image')
        if image:
            product.image = image
        
        product.is_active = 'is_active' in request.POST
        product.is_featured = 'is_featured' in request.POST
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('shop:product_management')
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'shop/product_edit.html', context)