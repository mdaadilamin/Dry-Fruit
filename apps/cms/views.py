from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Banner, Testimonial, Page, ContactInfo, Newsletter, Enquiry
import json
import uuid

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
        # Check if we're editing an existing testimonial
        testimonial_id = request.POST.get('testimonial_id')
        if testimonial_id:
            # Editing existing testimonial
            if not request.user.has_permission('cms', 'edit'):
                messages.error(request, 'Access denied.')
                return redirect('cms:testimonial_management')
            
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.customer_name = request.POST.get('customer_name', testimonial.customer_name)
            testimonial.rating = int(request.POST.get('rating', testimonial.rating))
            testimonial.comment = request.POST.get('comment', testimonial.comment)
            testimonial.location = request.POST.get('location', testimonial.location)
            # Fix the is_active handling - when checkbox is unchecked, it won't be in POST data
            testimonial.is_active = 'is_active' in request.POST
            
            if 'customer_image' in request.FILES:
                testimonial.customer_image = request.FILES['customer_image']
                
            testimonial.save()
            messages.success(request, 'Testimonial updated successfully!')
        else:
            # Adding new testimonial
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
                    customer_image=customer_image,
                    is_active='is_active' in request.POST  # Fix the is_active handling
                )
                messages.success(request, 'Testimonial added successfully!')
            else:
                messages.error(request, 'Please fill all required fields.')
    
    testimonials = Testimonial.objects.all()
    return render(request, 'cms/testimonial_management.html', {'testimonials': testimonials})


@login_required
def delete_testimonial(request, testimonial_id):
    """Delete a testimonial"""
    if not request.user.has_permission('cms', 'delete'):
        messages.error(request, 'Access denied.')
        return redirect('cms:testimonial_management')
    
    if request.method == 'POST':
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully!')
    
    return redirect('cms:testimonial_management')


def submit_testimonial(request):
    """Customer testimonial submission"""
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        location = request.POST.get('location', '')
        customer_image = request.FILES.get('customer_image')
        
        if all([customer_name, rating, comment]):
            # Create testimonial with is_active=False by default (requires admin approval)
            Testimonial.objects.create(
                customer_name=customer_name,
                rating=int(rating),
                comment=comment,
                location=location,
                customer_image=customer_image,
                is_active=False  # Requires admin approval
            )
            messages.success(request, 'Thank you for your testimonial! It will be reviewed and published shortly.')
            return redirect('cms:page_view', page_type='about')  # Redirect to about page or wherever appropriate
        else:
            messages.error(request, 'Please fill all required fields.')
    
    return redirect('cms:page_view', page_type='about')

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
            'email': 'info@dryfruitsdelight.com',
            'phone': '+91-8309232756',
            'address': 'Shop no 4 , QMAKS Ayzal Residency , S.A. Colony , Tolichowki, Hyderabad -500008',
            'city': 'Hyderabad',
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
    elif page_type == 'shipping':
        template = 'cms/shipping.html'
    elif page_type == 'careers':
        # Get dynamic content for careers page
        from .models import CareersSection, CareersCultureItem, CareersTestimonial, CareersBenefit, CareersJobOpening
        template = 'cms/careers.html'
        return render(request, template, {
            'page': page,
            'careers_sections': CareersSection.objects.filter(is_active=True),
            'culture_items': CareersCultureItem.objects.filter(is_active=True),
            'testimonials': CareersTestimonial.objects.filter(is_active=True),
            'benefits': CareersBenefit.objects.filter(is_active=True),
            'job_openings': CareersJobOpening.objects.filter(is_active=True),
        })
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
        
        # Create newsletter subscription with is_active=False by default
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={
                'is_active': False,
                'confirmation_token': uuid.uuid4()
            }
        )
        
        if created:
            # Send confirmation email (in a real application, you would send an actual email)
            # For now, we'll just return a success message
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing! Please check your email to confirm your subscription.'
            })
        elif not newsletter.is_active:
            return JsonResponse({
                'success': False,
                'message': 'Please check your email to confirm your subscription.'
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

def confirm_newsletter_subscription(request, token):
    """Confirm newsletter subscription"""
    try:
        newsletter = get_object_or_404(Newsletter, confirmation_token=token)
        
        if newsletter.is_active:
            messages.info(request, 'Your subscription is already confirmed.')
        else:
            newsletter.confirm_subscription()
            messages.success(request, 'Thank you for confirming your newsletter subscription!')
        
        return redirect('core:home')
    
    except Exception as e:
        messages.error(request, 'Invalid confirmation link.')
        return redirect('core:home')

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

@require_POST
def submit_enquiry(request):
    """Handle customer enquiry submissions"""
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate required fields
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('cms:page_view', page_type='contact')
        
        # Create enquiry
        from .models import Enquiry
        enquiry = Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Send notification to admins
        from apps.users.models import User
        from apps.notifications.models import Notification
        from apps.notifications.services import EmailService
        from django.conf import settings
        
        # Get admin users
        admin_users = User.objects.filter(role__name='admin', is_active=True)
        
        # Create in-app notifications for admins
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                title=f'New Customer Enquiry: {subject}',
                message=f'From {name} ({email}): {message[:100]}...',
                notification_type='info'
            )
        
        # Send email notifications to admins
        for admin in admin_users:
            if admin.email:
                context = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'subject': subject,
                    'message': message,
                    'enquiry_id': enquiry.id
                }
                EmailService.send_email('new_enquiry', admin.email, context)
        
        messages.success(request, 'Thank you for your enquiry! We will get back to you soon.')
        
    except Exception as e:
        messages.error(request, 'An error occurred while submitting your enquiry. Please try again.')
    
    return redirect('cms:page_view', page_type='contact')

@login_required
def enquiry_management(request):
    """Manage customer enquiries"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    subject_filter = request.GET.get('subject', 'all')
    
    # Get enquiries
    enquiries = Enquiry.objects.all()
    
    # Apply filters
    if status_filter == 'resolved':
        enquiries = enquiries.filter(is_resolved=True)
    elif status_filter == 'unresolved':
        enquiries = enquiries.filter(is_resolved=False)
    
    if subject_filter != 'all':
        enquiries = enquiries.filter(subject=subject_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(enquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'enquiries': page_obj,
        'status_filter': status_filter,
        'subject_filter': subject_filter,
        'subject_choices': Enquiry.SUBJECT_CHOICES,
    }
    return render(request, 'cms/enquiry_management.html', context)

@login_required
def resolve_enquiry(request, enquiry_id):
    """Mark an enquiry as resolved"""
    if not request.user.has_permission('cms', 'edit'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        from .models import Enquiry
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        enquiry.resolve()
        messages.success(request, f'Enquiry from {enquiry.name} marked as resolved.')
    
    return redirect('cms:enquiry_management')

@login_required
def careers_section_management(request):
    """Manage careers page sections"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        from .models import CareersSection
        section_id = request.POST.get('section_id')
        if section_id:
            # Edit existing section
            section = get_object_or_404(CareersSection, id=section_id)
        else:
            # Create new section
            section = CareersSection()
        
        section.section_type = request.POST.get('section_type')
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        section.content = request.POST.get('content', '')
        section.order = int(request.POST.get('order', 0))
        section.is_active = bool(request.POST.get('is_active', True))
        section.save()
        messages.success(request, 'Section saved successfully!')
    
    from .models import CareersSection
    sections = CareersSection.objects.all().order_by('section_type', 'order')
    section_types = CareersSection.SECTION_TYPES
    
    return render(request, 'cms/careers_section_management.html', {
        'sections': sections,
        'section_types': section_types
    })

@login_required
def careers_culture_management(request):
    """Manage careers culture items"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        from .models import CareersCultureItem
        item_id = request.POST.get('item_id')
        if item_id:
            # Edit existing item
            item = get_object_or_404(CareersCultureItem, id=item_id)
        else:
            # Create new item
            item = CareersCultureItem()
        
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.icon_name = request.POST.get('icon_name')
        item.order = int(request.POST.get('order', 0))
        item.is_active = bool(request.POST.get('is_active', True))
        item.save()
        messages.success(request, 'Culture item saved successfully!')
    
    from .models import CareersCultureItem
    culture_items = CareersCultureItem.objects.all().order_by('order')
    
    return render(request, 'cms/careers_culture_management.html', {
        'culture_items': culture_items
    })

@login_required
def careers_testimonial_management(request):
    """Manage careers testimonials"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        from .models import CareersTestimonial
        testimonial_id = request.POST.get('testimonial_id')
        if testimonial_id:
            # Edit existing testimonial
            testimonial = get_object_or_404(CareersTestimonial, id=testimonial_id)
        else:
            # Create new testimonial
            testimonial = CareersTestimonial()
        
        testimonial.name = request.POST.get('name')
        testimonial.position = request.POST.get('position')
        testimonial.testimonial = request.POST.get('testimonial')
        testimonial.order = int(request.POST.get('order', 0))
        testimonial.is_active = bool(request.POST.get('is_active', True))
        testimonial.save()
        messages.success(request, 'Testimonial saved successfully!')
    
    from .models import CareersTestimonial
    testimonials = CareersTestimonial.objects.all().order_by('order')
    
    return render(request, 'cms/careers_testimonial_management.html', {
        'testimonials': testimonials
    })

@login_required
def careers_benefit_management(request):
    """Manage careers benefits"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        from .models import CareersBenefit
        benefit_id = request.POST.get('benefit_id')
        if benefit_id:
            # Edit existing benefit
            benefit = get_object_or_404(CareersBenefit, id=benefit_id)
        else:
            # Create new benefit
            benefit = CareersBenefit()
        
        benefit.title = request.POST.get('title')
        benefit.description = request.POST.get('description')
        benefit.icon_name = request.POST.get('icon_name')
        benefit.order = int(request.POST.get('order', 0))
        benefit.is_active = bool(request.POST.get('is_active', True))
        benefit.save()
        messages.success(request, 'Benefit saved successfully!')
    
    from .models import CareersBenefit
    benefits = CareersBenefit.objects.all().order_by('order')
    
    return render(request, 'cms/careers_benefit_management.html', {
        'benefits': benefits
    })

@login_required
def careers_opening_management(request):
    """Manage job openings"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        from .models import CareersJobOpening
        opening_id = request.POST.get('opening_id')
        if opening_id:
            # Edit existing opening
            opening = get_object_or_404(CareersJobOpening, id=opening_id)
        else:
            # Create new opening
            opening = CareersJobOpening()
        
        opening.title = request.POST.get('title')
        opening.department = request.POST.get('department')
        opening.location = request.POST.get('location')
        opening.description = request.POST.get('description')
        opening.responsibilities = request.POST.get('responsibilities', '')
        opening.requirements = request.POST.get('requirements', '')
        opening.order = int(request.POST.get('order', 0))
        opening.is_active = bool(request.POST.get('is_active', True))
        opening.save()
        messages.success(request, 'Job opening saved successfully!')
    
    from .models import CareersJobOpening
    openings = CareersJobOpening.objects.all().order_by('order')
    
    return render(request, 'cms/careers_opening_management.html', {
        'openings': openings
    })
