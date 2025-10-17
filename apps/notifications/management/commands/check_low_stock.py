from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.shop.models import Product
from apps.users.models import User
from apps.notifications.models import Notification
from apps.notifications.services import EmailService
from django.conf import settings

class Command(BaseCommand):
    help = 'Check for low stock products and send notifications to admins and customers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--threshold',
            type=int,
            default=10,
            help='Stock threshold for low stock alerts (default: 10)'
        )

    def handle(self, *args, **options):
        threshold = options['threshold']
        low_stock_products = Product.objects.filter(stock__lte=threshold, is_active=True)
        
        if not low_stock_products.exists():
            self.stdout.write(
                self.style.SUCCESS('No low stock products found.')
            )
            return

        # Get admin users
        admin_users = [user for user in User.objects.filter(is_active=True) if user.is_admin]
        
        if not admin_users:
            self.stdout.write(
                self.style.WARNING('No admin users found.')
            )
            return
        
        # Notify admins
        admin_count = 0
        for product in low_stock_products:
            # Create in-app notification for admins
            for admin in admin_users:
                Notification.objects.get_or_create(
                    user=admin,
                    title=f'Low Stock Alert: {product.name}',
                    message=f'The product "{product.name}" is running low on stock. Current stock: {product.stock} units.',
                    notification_type='warning'
                )
            
            # Send email notification to admins
            for admin in admin_users:
                if admin.email:
                    context = {
                        'product_name': product.name,
                        'current_stock': product.stock,
                        'threshold': threshold,
                        'product_url': f"http://localhost:8000{product.get_absolute_url()}"
                    }
                    EmailService.send_email('low_stock_alert', admin.email, context)
            
            admin_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent low stock notifications for {admin_count} products to {len(admin_users)} admins.'
            )
        )