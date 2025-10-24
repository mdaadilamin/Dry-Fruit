from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SystemNotification
from .services import NotificationService
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=SystemNotification)
def create_user_notifications_on_system_notification_save(sender, instance, created, **kwargs):
    """Create individual user notifications when a SystemNotification is created"""
    if created and instance.show_to_users:
        try:
            count = NotificationService.convert_system_to_user_notifications(instance)
            logger.info(f"Created {count} user notifications for system notification '{instance.title}'")
        except Exception as e:
            logger.error(f"Failed to create user notifications for system notification '{instance.title}': {str(e)}")