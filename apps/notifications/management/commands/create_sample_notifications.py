from django.core.management.base import BaseCommand
from apps.notifications.models import SystemNotification
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample system notifications for testing'

    def handle(self, *args, **options):
        # Create a promotion notification
        SystemNotification.objects.get_or_create(
            title='Summer Sale - 20% Off',
            message='Get 20% off on all dry fruits and nuts for a limited time only!',
            notification_type='promotion',
            is_active=True,
            show_to_users=True,
            show_to_guests=True,
            valid_until=timezone.now() + timedelta(days=7)
        )

        # Create a new arrival notification
        SystemNotification.objects.get_or_create(
            title='New Organic Collection',
            message='Check out our new organic collection of premium nuts and dried fruits!',
            notification_type='new_arrival',
            is_active=True,
            show_to_users=True,
            show_to_guests=True
        )

        # Create an announcement
        SystemNotification.objects.get_or_create(
            title='Free Shipping Extended',
            message='We\'ve extended our free shipping offer to all orders over $50!',
            notification_type='announcement',
            is_active=True,
            show_to_users=True,
            show_to_guests=True
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample system notifications')
        )