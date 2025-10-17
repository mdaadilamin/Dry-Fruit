from django.core.management.base import BaseCommand
from apps.shop.models import Product, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create sample products for Chocolates and Spices categories for testing'

    def handle(self, *args, **options):
        # Get the categories
        try:
            chocolates_category = Category.objects.get(name='Chocolates')
            spices_category = Category.objects.get(name='Spices')
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Chocolates or Spices category not found. Please create them first.')
            )
            return

        # Create sample products for Chocolates
        chocolates_products = [
            {
                'name': 'Premium Dark Chocolate',
                'description': 'Rich and decadent dark chocolate made from premium cocoa beans',
                'price': 8.99,
                'stock': 50,
                'category': chocolates_category,
                'is_active': True
            },
            {
                'name': 'Milk Chocolate Truffles',
                'description': 'Delicious milk chocolate truffles with a smooth, creamy center',
                'price': 12.99,
                'stock': 30,
                'category': chocolates_category,
                'is_active': True
            },
            {
                'name': 'White Chocolate Bar',
                'description': 'Smooth and creamy white chocolate bar with hints of vanilla',
                'price': 7.99,
                'stock': 40,
                'category': chocolates_category,
                'is_active': True
            }
        ]

        # Create sample products for Spices
        spices_products = [
            {
                'name': 'Organic Cinnamon',
                'description': 'High-quality organic cinnamon sourced from Sri Lanka',
                'price': 5.99,
                'stock': 30,
                'category': spices_category,
                'is_active': True
            },
            {
                'name': 'Ground Turmeric',
                'description': 'Freshly ground turmeric with vibrant color and earthy flavor',
                'price': 4.99,
                'stock': 25,
                'category': spices_category,
                'is_active': True
            },
            {
                'name': 'Black Peppercorns',
                'description': 'Whole black peppercorns with bold, pungent flavor',
                'price': 3.99,
                'stock': 35,
                'category': spices_category,
                'is_active': True
            }
        ]

        created_count = 0
        for product_data in chocolates_products + spices_products:
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
                f'Successfully created {created_count} sample products for Chocolates and Spices categories'
            )
        )