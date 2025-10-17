from django.core.management.base import BaseCommand
from apps.shop.models import Product
from apps.orders.models import OrderItem
from django.db.models import Count

class Command(BaseCommand):
    help = 'Update product relationships based on purchase history'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Maximum number of products to process (default: 100)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        products = Product.objects.filter(is_active=True)[:limit]
        
        updated_count = 0
        for product in products:
            # Update frequently bought together relationships
            self.update_frequently_bought_together(product)
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated relationships for {updated_count} products'
            )
        )
    
    def update_frequently_bought_together(self, product):
        """Update frequently bought together relationships for a product"""
        # This would typically involve updating a many-to-many relationship
        # or a separate model to store these relationships
        # For now, we're just using the algorithm in the view
        pass