from django.core.management.base import BaseCommand
from apps.cms.models import HomePageHero, FooterContent, HomePageFeature

class Command(BaseCommand):
    help = 'Populate CMS with initial dynamic content'

    def handle(self, *args, **options):
        # Create homepage hero content
        HomePageHero.objects.get_or_create(
            title="Premium Dry Fruits & Nuts",
            subtitle="",
            description="Discover the finest selection of organic, hand-picked dry fruits and nuts from around the world. Quality, taste, and nutrition in every bite.",
            button_text="Shop Now",
            button_link="core:shop",
            is_active=True,
            order=0
        )

        # Create footer content
        FooterContent.objects.get_or_create(
            business_name="DRY FRUITS DELIGHT",
            copyright_text="© 2024 DRY FRUITS DELIGHT. All rights reserved.",
            address="Shop no 4 , QMAKS Ayzal Residency , S.A. Colony , Tolichowki, Hyderabad -500008",
            phone="+91-8309232756",
            email="info@dryfruitsdelight.com",
            facebook_url="https://www.facebook.com/dryfruitsdelight",
            instagram_url="https://www.instagram.com/dryfruitsdelight",
            twitter_url="https://www.twitter.com/dryfruitsdelight",
            youtube_url="https://www.youtube.com/dryfruitsdelight",
            is_active=True
        )

        # Create homepage features
        features_data = [
            {
                "title": "100% Organic",
                "description": "All our products are certified organic and free from harmful chemicals and pesticides.",
                "icon_name": "leaf",
                "order": 1
            },
            {
                "title": "Premium Quality",
                "description": "Hand-picked and carefully selected products to ensure the highest quality and freshness.",
                "icon_name": "award",
                "order": 2
            },
            {
                "title": "Fast Delivery",
                "description": "Quick and secure delivery to ensure your products reach you fresh and on time.",
                "icon_name": "truck",
                "order": 3
            },
            {
                "title": "Quality Assurance",
                "description": "Rigorous quality checks at every step to maintain our high standards.",
                "icon_name": "shield-check",
                "order": 4
            },
            {
                "title": "Health Benefits",
                "description": "Rich in nutrients, vitamins, and minerals for your healthy lifestyle.",
                "icon_name": "heart",
                "order": 5
            },
            {
                "title": "Customer Support",
                "description": "Dedicated customer service team to assist you with any queries or concerns.",
                "icon_name": "users",
                "order": 6
            }
        ]

        for feature_data in features_data:
            HomePageFeature.objects.get_or_create(
                title=feature_data["title"],
                defaults={
                    "description": feature_data["description"],
                    "icon_name": feature_data["icon_name"],
                    "order": feature_data["order"],
                    "is_active": True
                }
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated dynamic content')
        )