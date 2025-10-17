from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmailTemplate, SMSTemplate, EmailLog, SMSLog

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