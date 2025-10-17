from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Banner, Testimonial, Page, ContactInfo, Newsletter
import json

@login_required
def banner_management(request):
    """Banner management page"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    banners = Banner.objects.all()
    return render(request, 'cms/banner_management.html', {'banners': banners})

@login_required
def testimonial_management(request):
    """Testimonial management page"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'add'):
        customer_name = request.POST.get('customer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        location = request.POST.get('location', '')
        customer_image = request.FILES.get('customer_image')
        
        if all([customer_name, rating, comment]):
            Testimonial.objects.create(
                customer_name=customer_name,
                rating=int(rating),
                comment=comment,
                location=location,
                customer_image=customer_image
            )
            messages.success(request, 'Testimonial added successfully!')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    testimonials = Testimonial.objects.all()
    return render(request, 'cms/testimonial_management.html', {'testimonials': testimonials})

@login_required
def page_management(request):
    """Page content management"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    page_type = request.GET.get('page', 'about')
    page, created = Page.objects.get_or_create(
        page_type=page_type,
        defaults={
            'title': page_type.replace('_', ' ').title(),
            'content': f'Content for {page_type} page'
        }
    )
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        page.title = request.POST.get('title', page.title)
        page.content = request.POST.get('content', page.content)
        page.meta_description = request.POST.get('meta_description', page.meta_description)
        page.save()
        messages.success(request, 'Page updated successfully!')
    
    context = {
        'page': page,
        'page_choices': Page.PAGE_CHOICES,
        'current_page': page_type,
    }
    return render(request, 'cms/page_management.html', context)

@login_required
def contact_management(request):
    """Contact information management"""
    if not request.user.has_permission('cms', 'edit'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,  # Ensure only one contact info record
        defaults={
            'email': 'info@nutriharvest.com',
            'phone': '+1-234-567-8900',
            'address': '123 Business Street',
            'city': 'Business City',
            'pincode': '123456'
        }
    )
    
    if request.method == 'POST':
        contact_info.business_name = request.POST.get('business_name', contact_info.business_name)
        contact_info.tagline = request.POST.get('tagline', contact_info.tagline)
        contact_info.email = request.POST.get('email', contact_info.email)
        contact_info.phone = request.POST.get('phone', contact_info.phone)
        contact_info.whatsapp = request.POST.get('whatsapp', contact_info.whatsapp)
        contact_info.address = request.POST.get('address', contact_info.address)
        contact_info.city = request.POST.get('city', contact_info.city)
        contact_info.pincode = request.POST.get('pincode', contact_info.pincode)
        contact_info.facebook_url = request.POST.get('facebook_url', contact_info.facebook_url)
        contact_info.instagram_url = request.POST.get('instagram_url', contact_info.instagram_url)
        contact_info.twitter_url = request.POST.get('twitter_url', contact_info.twitter_url)
        contact_info.youtube_url = request.POST.get('youtube_url', contact_info.youtube_url)
        contact_info.business_hours = request.POST.get('business_hours', contact_info.business_hours)
        contact_info.save()
        messages.success(request, 'Contact information updated successfully!')
    
    return render(request, 'cms/contact_management.html', {'contact_info': contact_info})

def page_view(request, page_type):
    """Display CMS pages"""
    page = get_object_or_404(Page, page_type=page_type, is_active=True)
    
    # Use specific templates for certain pages
    if page_type == 'about':
        template = 'cms/about.html'
    elif page_type == 'contact':
        # Get contact information for the contact page
        from .models import ContactInfo
        contact_info, created = ContactInfo.objects.get_or_create(id=1)
        template = 'cms/contact.html'
        return render(request, template, {'page': page, 'contact_info': contact_info})
    elif page_type == 'returns':
        template = 'cms/returns.html'
    elif page_type == 'privacy':
        template = 'cms/privacy.html'
    elif page_type == 'terms':
        template = 'cms/terms.html'
    else:
        template = 'cms/page.html'
    
    return render(request, template, {'page': page})

@require_POST
def newsletter_subscribe(request):
    """Newsletter subscription"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required'
            })
        
        newsletter, created = Newsletter.objects.get_or_create(email=email)
        
        if created:
            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed to newsletter!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Email already subscribed'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred during subscription'
        })

@require_POST
def submit_return_request(request):
    """Handle return request submission"""
    try:
        data = json.loads(request.body)
        order_number = data.get('orderNumber')
        email = data.get('email')
        reason = data.get('reason')
        details = data.get('details')
        
        # Validate required fields
        if not all([order_number, email, reason]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            })
        
        # In a real application, you would:
        # 1. Validate the order number exists
        # 2. Validate the email matches the order
        # 3. Save the return request to the database
        # 4. Send confirmation emails
        
        # For now, we'll just simulate success
        return JsonResponse({
            'success': True,
            'message': f'Thank you for submitting your return request for order #{order_number}. We\'ve sent a confirmation email to {email}. You\'ll receive your Return Merchandise Authorization (RMA) number within 24 hours.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your return request. Please try again.'
        })