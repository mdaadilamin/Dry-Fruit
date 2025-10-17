from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.db import models
from .models import EmailTemplate, SMSTemplate, EmailLog, SMSLog, SystemNotification, Notification

@login_required
def email_template_management(request):
    """Email template management"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    template_type = request.GET.get('template', 'order_confirmation')
    template, created = EmailTemplate.objects.get_or_create(
        template_type=template_type,
        defaults={
            'subject': f'{template_type.replace("_", " ").title()} - NutriHarvest',
            'body_html': f'<h1>{template_type.replace("_", " ").title()}</h1><p>Default template content</p>',
            'body_text': f'{template_type.replace("_", " ").title()}\n\nDefault template content'
        }
    )
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        template.subject = request.POST.get('subject', template.subject)
        template.body_html = request.POST.get('body_html', template.body_html)
        template.body_text = request.POST.get('body_text', template.body_text)
        template.is_active = 'is_active' in request.POST
        template.save()
        messages.success(request, 'Email template updated successfully!')
    
    context = {
        'template': template,
        'template_choices': EmailTemplate.TEMPLATE_TYPES,
        'current_template': template_type,
    }
    return render(request, 'notifications/email_template_management.html', context)

@login_required
def sms_template_management(request):
    """SMS template management"""
    if not request.user.has_permission('cms', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    templates = SMSTemplate.objects.all()
    
    if request.method == 'POST' and request.user.has_permission('cms', 'edit'):
        template_id = request.POST.get('template_id')
        template = get_object_or_404(SMSTemplate, id=template_id)
        template.message = request.POST.get('message', template.message)
        template.is_active = 'is_active' in request.POST
        template.save()
        messages.success(request, 'SMS template updated successfully!')
    
    return render(request, 'notifications/sms_template_management.html', {'templates': templates})

@login_required
def email_log(request):
    """Email log view"""
    if not request.user.has_permission('reports', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    logs = EmailLog.objects.order_by('-created_at')[:100]
    return render(request, 'notifications/email_log.html', {'logs': logs})

@login_required
def sms_log(request):
    """SMS log view"""
    if not request.user.has_permission('reports', 'view'):
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    logs = SMSLog.objects.order_by('-created_at')[:100]
    return render(request, 'notifications/sms_log.html', {'logs': logs})


@require_GET
def get_system_notifications(request):
    """Get active system notifications for display"""
    # Get active notifications that are valid
    notifications = SystemNotification.objects.filter(
        is_active=True,
        created_at__lte=timezone.now()
    ).filter(
        models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=timezone.now())
    )
    
    # Filter based on user authentication status
    if request.user.is_authenticated:
        notifications = notifications.filter(show_to_users=True)
    else:
        notifications = notifications.filter(show_to_guests=True)
    
    # Convert to JSON format
    notification_data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'created_at': n.created_at.isoformat(),
        }
        for n in notifications
    ]
    
    return JsonResponse({
        'success': True,
        'notifications': notification_data
    })


@require_GET
def get_user_notifications(request):
    """Get user notifications"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Authentication required'
        }, status=401)
    
    # Get user's 10 most recent notifications
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    # Convert to JSON format
    notification_data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
        }
        for n in notifications
    ]
    
    return JsonResponse({
        'success': True,
        'notifications': notification_data
    })