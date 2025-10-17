from django.contrib import admin
from .models import EmailTemplate, EmailLog, SMSTemplate, SMSLog, Notification

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_type', 'subject', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['subject', 'body_html']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'subject', 'template_type', 'status', 'sent_at']
    list_filter = ['status', 'template_type', 'created_at']
    search_fields = ['recipient', 'subject']
    readonly_fields = ['created_at', 'sent_at']

@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_type', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'template_type', 'status', 'sent_at']
    list_filter = ['status', 'template_type', 'created_at']
    search_fields = ['recipient']
    readonly_fields = ['created_at', 'sent_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']