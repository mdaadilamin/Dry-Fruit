import os
import django
from django.conf import settings
from apps.cms.models import Banner

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriharvest.settings')
django.setup()

# Create a test banner
banner = Banner.objects.create(
    title="Test Banner",
    subtitle="Test Subtitle",
    description="Test Description",
    button_text="Shop Now",
    button_link="/shop/",
    is_active=True,
    order=1
)

print(f"Banner created successfully: {banner.title}")
print(f"Total banners: {Banner.objects.count()}")