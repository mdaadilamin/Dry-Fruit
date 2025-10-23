from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.text import slugify
from .models import Product, Category, ProductReview, ProductVariant, ProductImage
from apps.users.models import User
from django.utils import timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

@login_required
def product_management(request):
    """Product management page (Admin/Employee only)"""
    if not request.user.has_permission('products', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    products: 'QuerySet[Product]' = Product.objects.select_related('category').all()
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
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Add new category
        if action == 'add' and request.user.has_permission('products', 'add'):
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == 'on'
            image = request.FILES.get('image')
            
            if name:
                Category.objects.create(
                    name=name,
                    description=description,
                    is_active=is_active,
                    image=image
                )
                messages.success(request, 'Category added successfully!')
            else:
                messages.error(request, 'Category name is required.')
        
        # Edit existing category
        elif action == 'edit' and request.user.has_permission('products', 'edit'):
            category_id = request.POST.get('id')
            category = get_object_or_404(Category, id=category_id)
            
            category.name = request.POST.get('name', category.name)
            category.description = request.POST.get('description', category.description)
            category.is_active = request.POST.get('is_active') == 'on'
            
            image = request.FILES.get('image')
            if image:
                category.image = image
            
            category.save()
            messages.success(request, 'Category updated successfully!')
        
        # Delete category
        elif action == 'delete' and request.user.has_permission('products', 'delete'):
            category_id = request.POST.get('id')
            category = get_object_or_404(Category, id=category_id)
            
            # Store category name for message before deletion
            category_name = category.name
            category.delete()
            messages.success(request, f'Category "{category_name}" deleted successfully!')
        
        return redirect('shop:category_management')
    
    categories: 'QuerySet[Category]' = Category.objects.all()
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
        meta_title = request.POST.get('meta_title', '')
        meta_description = request.POST.get('meta_description', '')
        keywords = request.POST.get('keywords', '')
        tags = request.POST.get('tags', '')
        discount_percent = request.POST.get('discount_percent', 0.00)
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        if all([name, category_id, price, stock, description]):
            try:
                category = Category.objects.get(id=category_id)
                
                # Generate a unique slug
                slug = slugify(name)
                counter = 1
                original_slug = slug
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                Product.objects.create(
                    name=name,
                    slug=slug,
                    category=category,
                    price=price,
                    stock=stock,
                    description=description,
                    nutritional_info=nutritional_info,
                    image=image,
                    meta_title=meta_title,
                    meta_description=meta_description,
                    keywords=keywords,
                    tags=tags,
                    discount_percent=discount_percent,
                    is_active=is_active,
                    is_featured=is_featured
                )
                messages.success(request, 'Product added successfully!')
                return redirect('shop:product_management')
            except Category.DoesNotExist:
                messages.error(request, 'Invalid category selected.')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    categories: 'QuerySet[Category]' = Category.objects.filter(is_active=True)
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
        product.meta_title = request.POST.get('meta_title', product.meta_title)
        product.meta_description = request.POST.get('meta_description', product.meta_description)
        product.keywords = request.POST.get('keywords', product.keywords)
        product.tags = request.POST.get('tags', product.tags)
        product.discount_percent = request.POST.get('discount_percent', product.discount_percent)
        product.is_active = request.POST.get('is_active') == 'on'
        product.is_featured = request.POST.get('is_featured') == 'on'
        
        # Update slug if name changed
        if product.name != request.POST.get('name', product.name):
            slug = slugify(product.name)
            counter = 1
            original_slug = slug
            while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            product.slug = slug
        
        image = request.FILES.get('image')
        if image:
            product.image = image
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('shop:product_management')
    
    categories: 'QuerySet[Category]' = Category.objects.filter(is_active=True)
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'shop/product_edit.html', context)

@login_required
def review_management(request):
    """Manage product reviews (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')
        
        if review_id and action:
            review = get_object_or_404(ProductReview, id=review_id)
            
            if action == 'approve':
                review.is_approved = True
                review.save()
                messages.success(request, f'Review by {review.user.full_name} approved successfully!')
            elif action == 'reject':
                review.delete()
                messages.success(request, f'Review by {review.user.full_name} rejected and deleted!')
            elif action == 'verify':
                review.is_verified = True
                review.save()
                messages.success(request, f'Review by {review.user.full_name} marked as verified!')
    
    # Get all reviews, approved and pending
    reviews: 'QuerySet[ProductReview]' = ProductReview.objects.select_related('product', 'user').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reviews': page_obj,
    }
    return render(request, 'shop/review_management.html', context)

@login_required
def submit_review(request, product_id):
    """Submit a product review via AJAX"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            rating = data.get('rating')
            comment = data.get('comment')
            
            product = get_object_or_404(Product, id=product_id)
            
            # Check if user has already reviewed this product
            review, created = ProductReview.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': rating,
                    'comment': comment,
                    'is_verified': False,  # Could be set to True if user purchased the product
                    'is_approved': False   # Admin needs to approve reviews
                }
            )
            
            if not created:
                # Update existing review
                review.rating = rating
                review.comment = comment
                review.save()
                message = 'Your review has been updated successfully!'
            else:
                message = 'Your review has been submitted successfully! It will be visible after approval.'
            
            return JsonResponse({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while submitting your review. Please try again.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })