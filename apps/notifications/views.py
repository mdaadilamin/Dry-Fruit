from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from django.db import models
from .models import EmailTemplate, SMSTemplate, EmailLog, SMSLog, SystemNotification, Notification
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .management.commands.check_low_stock import Command as CheckLowStockCommand
from django.http import HttpResponseNotAllowed

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
            'subject': f'{template_type.replace("_", " ").title()} - DRY FRUITS DELIGHT',
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


@login_required
def system_notification_management(request):
    """Manage system notifications (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # Handle notification creation/update
        notification_id = request.POST.get('notification_id')
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        is_active = 'is_active' in request.POST
        show_to_users = 'show_to_users' in request.POST
        show_to_guests = 'show_to_guests' in request.POST
        valid_until = request.POST.get('valid_until')
        
        if notification_id:
            # Update existing notification
            notification = get_object_or_404(SystemNotification, id=notification_id)
            notification.title = title
            notification.message = message
            notification.notification_type = notification_type
            notification.is_active = is_active
            notification.show_to_users = show_to_users
            notification.show_to_guests = show_to_guests
            if valid_until:
                notification.valid_until = valid_until
            notification.save()
            messages.success(request, f'Notification "{title}" updated successfully!')
        else:
            # Create new notification
            if title and message:
                notification = SystemNotification.objects.create(
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    is_active=is_active,
                    show_to_users=show_to_users,
                    show_to_guests=show_to_guests,
                    valid_until=valid_until if valid_until else None
                )
                messages.success(request, f'Notification "{title}" created successfully!')
            else:
                messages.error(request, 'Title and message are required.')
        
        return redirect('notifications:system_notification_management')
    
    # Display notifications
    notifications = SystemNotification.objects.all().order_by('-created_at')
    context = {
        'notifications': notifications,
        'notification_types': SystemNotification.NOTIFICATION_TYPES,
    }
    return render(request, 'notifications/system_notification_management.html', context)


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


@staff_member_required
@require_http_methods(["POST"])
def check_low_stock_view(request):
    """Manual trigger for low stock check"""
    threshold = int(request.POST.get('threshold', 10))
    
    # Run the management command
    command = CheckLowStockCommand()
    command.handle(threshold=threshold)
    
    messages.success(request, f'Low stock check completed with threshold {threshold}.')
    return redirect('core:admin_panel')


@staff_member_required
@require_http_methods(["POST"])
def delete_system_notification(request, notification_id):
    """Delete a system notification"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    notification = get_object_or_404(SystemNotification, id=notification_id)
    
    # Delete related user notifications
    Notification.objects.filter(
        title=notification.title,
        message=notification.message,
        created_at=notification.created_at
    ).delete()
    
    # Delete the system notification
    notification.delete()
    
    messages.success(request, f'Notification "{notification.title}" deleted successfully!')
    return redirect('notifications:system_notification_management')


@login_required
def all_user_notifications(request):
    """Display all user notifications"""
    # Get all user notifications ordered by creation date
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Mark all as read when viewing
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/all_user_notifications.html', context)
