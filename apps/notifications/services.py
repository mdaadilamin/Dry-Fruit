from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EmailTemplate, EmailLog, SMSTemplate, SMSLog
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for handling email notifications"""
    
    @staticmethod
    def send_email(template_type, recipient, context=None):
        """Send email using template"""
        try:
            template = EmailTemplate.objects.get(template_type=template_type, is_active=True)
            
            if context is None:
                context = {}
            
            # Render email content
            subject = template.subject
            html_content = template.body_html
            text_content = template.body_text or strip_tags(html_content)
            
            # Replace placeholders with context data
            for key, value in context.items():
                subject = subject.replace(f'{{{key}}}', str(value))
                html_content = html_content.replace(f'{{{key}}}', str(value))
                text_content = text_content.replace(f'{{{key}}}', str(value))
            
            # Create email log
            email_log = EmailLog.objects.create(
                recipient=recipient,
                subject=subject,
                template_type=template_type
            )
            
            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                html_message=html_content,
                fail_silently=False
            )
            
            # Update log status
            email_log.status = 'sent'
            email_log.save()
            
            return True
            
        except EmailTemplate.DoesNotExist:
            logger.error(f"Email template '{template_type}' not found")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            if 'email_log' in locals():
                email_log.status = 'failed'
                email_log.error_message = str(e)
                email_log.save()
            return False

class SMSService:
    """Service for handling SMS notifications (placeholder implementation)"""
    
    @staticmethod
    def send_sms(template_type, recipient, context=None):
        """Send SMS using template (placeholder)"""
        try:
            template = SMSTemplate.objects.get(template_type=template_type, is_active=True)
            
            if context is None:
                context = {}
            
            # Prepare message
            message = template.message
            for key, value in context.items():
                message = message.replace(f'{{{key}}}', str(value))
            
            # Create SMS log
            sms_log = SMSLog.objects.create(
                recipient=recipient,
                message=message,
                template_type=template_type
            )
            
            # TODO: Implement actual SMS sending (Twilio, AWS SNS, etc.)
            # For now, just log the SMS
            logger.info(f"SMS to {recipient}: {message}")
            
            # Update log status
            sms_log.status = 'sent'
            sms_log.save()
            
            return True
            
        except SMSTemplate.DoesNotExist:
            logger.error(f"SMS template '{template_type}' not found")
            return False
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            if 'sms_log' in locals():
                sms_log.status = 'failed'
                sms_log.error_message = str(e)
                sms_log.save()
            return False

class WhatsAppService:
    """Service for handling WhatsApp notifications (placeholder)"""
    
    @staticmethod
    def send_whatsapp(recipient, message, template_name=None):
        """Send WhatsApp message (placeholder)"""
        try:
            # TODO: Implement WhatsApp Business API integration
            logger.info(f"WhatsApp to {recipient}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp: {str(e)}")
            return False