from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps

class Command(BaseCommand):
    help = 'Send notifications for new orders to admins and customers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-id',
            type=int,
            help='Specific order ID to send notification for'
        )
        parser.add_argument(
            '--minutes',
            type=int,
            default=5,
            help='Check for orders created within the last N minutes (default: 5)'
        )

    def handle(self, *args, **options):
        # Get models dynamically to avoid import issues
        Order = apps.get_model('orders', 'Order')
        User = apps.get_model('users', 'User')
        Notification = apps.get_model('notifications', 'Notification')
        
        if options['order_id']:
            # Process specific order
            try:
                order = Order.objects.get(id=options['order_id'])
                self.send_order_notifications(order, Notification, User)
                self.stdout.write(
                    'Successfully sent notifications for order #{}'.format(order.order_number)
                )
            except Order.DoesNotExist:
                self.stdout.write(
                    'Error: Order with ID {} not found'.format(options["order_id"])
                )
        else:
            # Process recent orders
            minutes = options['minutes']
            time_threshold = timezone.now() - timezone.timedelta(minutes=minutes)
            recent_orders = Order.objects.filter(
                created_at__gte=time_threshold
            ).order_by('-created_at')
            
            if not recent_orders.exists():
                self.stdout.write(
                    'No recent orders found.'
                )
                return
            
            processed_count = 0
            for order in recent_orders:
                self.send_order_notifications(order, Notification, User)
                processed_count += 1
            
            self.stdout.write(
                'Successfully sent notifications for {} recent orders.'.format(processed_count)
            )

    def send_order_notifications(self, order, Notification, User):
        """Send notifications for a new order"""
        # Get admin users
        admin_users = [user for user in User.objects.filter(is_active=True) if user.is_admin]
        
        # Import EmailService here to avoid import issues
        from apps.notifications.services import EmailService
        
        # Notify customer
        if order.customer.email:
            context = {
                'order_number': order.order_number,
                'customer_name': order.customer.full_name,
                'order_total': order.total_amount,
                'order_date': order.created_at.strftime('%B %d, %Y'),
                'order_items': [
                    {
                        'name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.price,
                        'total': item.get_total_price()
                    }
                    for item in order.items.all()
                ],
                'shipping_address': f"{order.shipping_address}, {order.shipping_city}, {order.shipping_pincode}",
                'order_url': f"http://localhost:8000/orders/{order.id}/"
            }
            EmailService.send_email('order_confirmation', order.customer.email, context)
        
        # Create in-app notification for customer
        Notification.objects.get_or_create(
            user=order.customer,
            title=f'Order #{order.order_number} Confirmed',
            message=f'Your order #{order.order_number} for ₹{order.total_amount} has been confirmed and is being processed.',
            notification_type='success'
        )
        
        # Notify admins
        if admin_users:
            admin_context = {
                'order_number': order.order_number,
                'customer_name': order.customer.full_name,
                'order_total': order.total_amount,
                'order_date': order.created_at.strftime('%B %d, %Y'),
                'order_url': f"http://localhost:8000/admin/orders/order/{order.id}/change/"
            }
            
            for admin in admin_users:
                # Create in-app notification for admins
                Notification.objects.get_or_create(
                    user=admin,
                    title=f'New Order #{order.order_number}',
                    message=f'New order from {order.customer.full_name} for ₹{order.total_amount}',
                    notification_type='info'
                )
                
                # Send email notification to admins
                if admin.email:
                    EmailService.send_email('order_confirmation', admin.email, admin_context)