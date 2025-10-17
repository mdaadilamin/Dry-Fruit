from django.core.management.base import BaseCommand
from apps.shop.models import Product, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create sample products with low stock for testing'

    def handle(self, *args, **options):
        # Get or create a category for testing
        category, created = Category.objects.get_or_create(
            name='Test Category',
            defaults={
                'description': 'Category for testing low stock notifications',
                'is_active': True
            }
        )
        
        # Create sample products with low stock
        low_stock_products = [
            {
                'name': 'Low Stock Almonds',
                'description': 'Premium almonds with low stock for testing notifications',
                'price': 12.99,
                'stock': 5,  # Low stock
                'category': category,
                'is_active': True
            },
            {
                'name': 'Low Stock Walnuts',
                'description': 'Organic walnuts with low stock for testing notifications',
                'price': 9.99,
                'stock': 3,  # Low stock
                'category': category,
                'is_active': True
            }
        ]
        
        created_count = 0
        for product_data in low_stock_products:
            # Add slug to product data
            product_data['slug'] = slugify(product_data['name'])
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample low stock products'
            )
        )