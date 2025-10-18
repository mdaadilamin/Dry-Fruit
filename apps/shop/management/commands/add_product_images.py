from django.core.management.base import BaseCommand
from apps.shop.models import Product
import os

class Command(BaseCommand):
    help = 'Instructions for adding product images'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "Product Image Management Instructions:\n"
                "=====================================\n\n"
                "To add images to products, you have two options:\n\n"
                "1. Manual Upload via Admin Panel:\n"
                "   - Go to http://127.0.0.1:8000/admin/\n"
                "   - Login with admin credentials (username: admin, password: admin123)\n"
                "   - Navigate to 'Products' under 'Shop'\n"
                "   - Click on each product and upload an image\n\n"
                "2. Programmatic Upload (for development):\n"
                "   - Place your product images in a directory\n"
                "   - Use Django's file handling to assign images to products\n\n"
                "Current product count: " + str(Product.objects.count()) + "\n"
                "Products without images: " + str(Product.objects.filter(image='').count()) + "\n\n"
                "Example code snippet for programmatic image assignment:\n"
                "---------------------------------------------\n"
                "from django.core.files import File\n"
                "product = Product.objects.get(name='California Almonds')\n"
                "with open('path/to/almonds.jpg', 'rb') as f:\n"
                "    product.image.save('california-almonds.jpg', File(f), save=True)\n"
                "---------------------------------------------\n\n"
                "For production, consider:\n"
                "- Using a CDN for image hosting\n"
                "- Implementing image optimization\n"
                "- Adding alt text for accessibility\n"
                "- Creating multiple image sizes for responsive design"
            )
        )
