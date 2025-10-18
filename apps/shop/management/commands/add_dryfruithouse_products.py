from django.core.management.base import BaseCommand
from apps.shop.models import Product, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Add products from the Dry Fruit House website'

    def handle(self, *args, **options):
        # Define products for each category
        products_data = {
            # Premium Nuts
            1: [
                {
                    'name': 'California Almonds',
                    'description': 'Premium quality almonds sourced directly from California orchards. Rich in vitamin E and healthy fats.',
                    'price': 12.99,
                    'stock': 100,
                    'nutritional_info': 'Calories: 579 per 100g, Protein: 21g, Fat: 50g, Carbs: 22g',
                    'tags': 'premium,healthy,snack'
                },
                {
                    'name': 'Organic Walnuts',
                    'description': 'Certified organic walnuts packed with omega-3 fatty acids and antioxidants.',
                    'price': 14.99,
                    'stock': 80,
                    'nutritional_info': 'Calories: 654 per 100g, Protein: 15g, Fat: 65g, Carbs: 14g',
                    'tags': 'organic,healthy,brain'
                },
                {
                    'name': 'Pistachios',
                    'description': 'Fresh pistachios with natural sea salt. A perfect healthy snack option.',
                    'price': 16.99,
                    'stock': 75,
                    'nutritional_info': 'Calories: 562 per 100g, Protein: 20g, Fat: 45g, Carbs: 28g',
                    'tags': 'premium,healthy,snack'
                },
                {
                    'name': 'Brazil Nuts',
                    'description': 'Large Brazil nuts rich in selenium, an essential mineral for immune function.',
                    'price': 18.99,
                    'stock': 60,
                    'nutritional_info': 'Calories: 659 per 100g, Protein: 14g, Fat: 67g, Carbs: 12g',
                    'tags': 'premium,healthy,immune'
                }
            ],
            
            # Dried Fruits
            2: [
                {
                    'name': 'Medjool Dates',
                    'description': 'Premium Medjool dates, naturally sweet and packed with fiber and potassium.',
                    'price': 9.99,
                    'stock': 90,
                    'nutritional_info': 'Calories: 277 per 100g, Protein: 2g, Fat: 0.4g, Carbs: 75g',
                    'tags': 'organic,natural,sweet'
                },
                {
                    'name': 'Dried Apricots',
                    'description': 'Sulfur-free dried apricots, rich in vitamin A and fiber.',
                    'price': 8.99,
                    'stock': 85,
                    'nutritional_info': 'Calories: 241 per 100g, Protein: 3.4g, Fat: 0.5g, Carbs: 63g',
                    'tags': 'organic,healthy,vitamin'
                },
                {
                    'name': 'Golden Raisins',
                    'description': 'Sweet and chewy golden raisins, perfect for baking and snacking.',
                    'price': 7.99,
                    'stock': 100,
                    'nutritional_info': 'Calories: 296 per 100g, Protein: 2.5g, Fat: 0.5g, Carbs: 79g',
                    'tags': 'natural,sweet,snack'
                },
                {
                    'name': 'Dried Figs',
                    'description': 'Whole dried figs with natural sweetness and chewy texture.',
                    'price': 11.99,
                    'stock': 70,
                    'nutritional_info': 'Calories: 255 per 100g, Protein: 3.3g, Fat: 1g, Carbs: 64g',
                    'tags': 'organic,natural,fiber'
                }
            ],
            
            # Seeds & Berries
            3: [
                {
                    'name': 'Chia Seeds',
                    'description': 'Organic chia seeds packed with omega-3 fatty acids, fiber, and protein.',
                    'price': 6.99,
                    'stock': 120,
                    'nutritional_info': 'Calories: 486 per 100g, Protein: 17g, Fat: 31g, Carbs: 42g',
                    'tags': 'organic,healthy,superfood'
                },
                {
                    'name': 'Goji Berries',
                    'description': 'Premium goji berries rich in antioxidants and vitamins.',
                    'price': 13.99,
                    'stock': 65,
                    'nutritional_info': 'Calories: 349 per 100g, Protein: 12g, Fat: 1g, Carbs: 77g',
                    'tags': 'organic,antioxidant,superfood'
                },
                {
                    'name': 'Pumpkin Seeds',
                    'description': 'Roasted pumpkin seeds rich in magnesium and zinc.',
                    'price': 5.99,
                    'stock': 95,
                    'nutritional_info': 'Calories: 559 per 100g, Protein: 30g, Fat: 49g, Carbs: 11g',
                    'tags': 'healthy,protein,magnesium'
                },
                {
                    'name': 'Sunflower Seeds',
                    'description': 'Hulled sunflower seeds with a delicious nutty flavor.',
                    'price': 4.99,
                    'stock': 110,
                    'nutritional_info': 'Calories: 584 per 100g, Protein: 21g, Fat: 51g, Carbs: 20g',
                    'tags': 'healthy,snack,protein'
                }
            ],
            
            # Gift Boxes
            4: [
                {
                    'name': 'Festival Special Gift Box',
                    'description': 'Premium gift box with a selection of our best-selling dry fruits and nuts. Perfect for festivals and celebrations.',
                    'price': 29.99,
                    'stock': 40,
                    'nutritional_info': 'Mixed nuts and dried fruits, varies by selection',
                    'tags': 'gift,festival,special'
                },
                {
                    'name': 'Executive Gift Box',
                    'description': 'Luxury gift box with premium nuts and exotic dried fruits. Ideal for corporate gifting.',
                    'price': 39.99,
                    'stock': 30,
                    'nutritional_info': 'Mixed premium nuts and dried fruits',
                    'tags': 'gift,luxury,corporate'
                },
                {
                    'name': 'Healthy Snacking Gift Box',
                    'description': 'Curated selection of healthy snacks including nuts, seeds, and dried fruits.',
                    'price': 24.99,
                    'stock': 50,
                    'nutritional_info': 'Mixed healthy snacks, varies by selection',
                    'tags': 'gift,healthy,snack'
                },
                {
                    'name': 'Diwali Celebration Box',
                    'description': 'Traditional Diwali gift box with a variety of dry fruits and nuts.',
                    'price': 34.99,
                    'stock': 35,
                    'nutritional_info': 'Traditional Indian dry fruits and nuts mix',
                    'tags': 'gift,festival,diwali'
                }
            ],
            
            # Organic Collection
            5: [
                {
                    'name': 'Organic Cashews',
                    'description': 'Certified organic cashews with creamy texture and rich flavor.',
                    'price': 15.99,
                    'stock': 75,
                    'nutritional_info': 'Calories: 553 per 100g, Protein: 18g, Fat: 44g, Carbs: 30g',
                    'tags': 'organic,healthy,premium'
                },
                {
                    'name': 'Organic Dried Mango',
                    'description': 'Sulfur-free organic dried mango slices with natural sweetness.',
                    'price': 12.99,
                    'stock': 60,
                    'nutritional_info': 'Calories: 320 per 100g, Protein: 1.5g, Fat: 0.5g, Carbs: 83g',
                    'tags': 'organic,natural,sweet'
                },
                {
                    'name': 'Organic Coconut Chips',
                    'description': 'Lightly salted organic coconut chips with crispy texture.',
                    'price': 9.99,
                    'stock': 80,
                    'nutritional_info': 'Calories: 592 per 100g, Protein: 6g, Fat: 57g, Carbs: 15g',
                    'tags': 'organic,healthy,coconut'
                },
                {
                    'name': 'Organic Mixed Nuts',
                    'description': 'Assorted organic nuts including almonds, walnuts, and cashews.',
                    'price': 17.99,
                    'stock': 70,
                    'nutritional_info': 'Mixed nuts, varies by selection',
                    'tags': 'organic,healthy,mixed'
                }
            ],
            
            # Chocolates
            7: [
                {
                    'name': 'Premium Dark Chocolate',
                    'description': 'Rich and decadent dark chocolate made from premium cocoa beans with 70% cocoa content.',
                    'price': 8.99,
                    'stock': 50,
                    'nutritional_info': 'Calories: 546 per 100g, Protein: 4.9g, Fat: 43g, Carbs: 48g',
                    'tags': 'premium,chocolate,dark'
                },
                {
                    'name': 'Milk Chocolate Truffles',
                    'description': 'Delicious milk chocolate truffles with a smooth, creamy center.',
                    'price': 12.99,
                    'stock': 30,
                    'nutritional_info': 'Calories: 538 per 100g, Protein: 5.5g, Fat: 33g, Carbs: 58g',
                    'tags': 'chocolate,sweet,premium'
                },
                {
                    'name': 'White Chocolate Bar',
                    'description': 'Smooth and creamy white chocolate bar with hints of vanilla.',
                    'price': 7.99,
                    'stock': 40,
                    'nutritional_info': 'Calories: 534 per 100g, Protein: 5.9g, Fat: 32g, Carbs: 59g',
                    'tags': 'chocolate,sweet,creamy'
                },
                {
                    'name': 'Chocolate Covered Almonds',
                    'description': 'Crunchy almonds covered in premium milk chocolate.',
                    'price': 10.99,
                    'stock': 60,
                    'nutritional_info': 'Calories: 520 per 100g, Protein: 11g, Fat: 35g, Carbs: 45g',
                    'tags': 'chocolate,nuts,sweet'
                }
            ],
            
            # Spices
            8: [
                {
                    'name': 'Organic Cinnamon',
                    'description': 'High-quality organic cinnamon sourced from Sri Lanka with warm, sweet flavor.',
                    'price': 5.99,
                    'stock': 30,
                    'nutritional_info': 'Calories: 247 per 100g, Protein: 4g, Fat: 1.2g, Carbs: 81g',
                    'tags': 'organic,spice,warm'
                },
                {
                    'name': 'Ground Turmeric',
                    'description': 'Freshly ground turmeric with vibrant color and earthy flavor.',
                    'price': 4.99,
                    'stock': 25,
                    'nutritional_info': 'Calories: 354 per 100g, Protein: 8g, Fat: 10g, Carbs: 65g',
                    'tags': 'organic,spice,anti-inflammatory'
                },
                {
                    'name': 'Black Peppercorns',
                    'description': 'Whole black peppercorns with bold, pungent flavor.',
                    'price': 3.99,
                    'stock': 35,
                    'nutritional_info': 'Calories: 251 per 100g, Protein: 10g, Fat: 3.3g, Carbs: 64g',
                    'tags': 'organic,spice,bold'
                },
                {
                    'name': 'Cardamom Pods',
                    'description': 'Premium cardamom pods with aromatic, slightly sweet flavor.',
                    'price': 8.99,
                    'stock': 20,
                    'nutritional_info': 'Calories: 311 per 100g, Protein: 11g, Fat: 7g, Carbs: 51g',
                    'tags': 'organic,spice,aromatic'
                }
            ]
        }
        
        created_count = 0
        updated_count = 0
        
        # Create or update products for each category
        for category_id, products in products_data.items():
            try:
                category = Category.objects.get(id=category_id)
                for product_data in products:
                    # Add required fields
                    product_data['category'] = category
                    product_data['is_active'] = True
                    product_data['is_featured'] = True
                    
                    # Handle slug uniqueness
                    base_slug = slugify(product_data['name'])
                    slug = base_slug
                    counter = 1
                    
                    # Check if product already exists
                    try:
                        product = Product.objects.get(name=product_data['name'], category=category)
                        # Update existing product
                        for key, value in product_data.items():
                            setattr(product, key, value)
                        product.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'Updated: {product.name} in {category.name}')
                        )
                    except Product.DoesNotExist:
                        # Create new product with unique slug
                        while Product.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        product_data['slug'] = slug
                        
                        product = Product.objects.create(**product_data)
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created: {product.name} in {category.name}')
                        )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Category with ID {category_id} not found')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {created_count + updated_count} products: '
                f'{created_count} created, {updated_count} updated'
            )
        )