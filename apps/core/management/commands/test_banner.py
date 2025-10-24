from django.core.management.base import BaseCommand
from apps.cms.models import Banner

class Command(BaseCommand):
    help = 'Test banner creation'

    def handle(self, *args, **options):
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

        self.stdout.write(
            self.style.SUCCESS(f'Banner created successfully: {banner.title}')
        )
        self.stdout.write(
            f'Total banners: {Banner.objects.count()}'
        )