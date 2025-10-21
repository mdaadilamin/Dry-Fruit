from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, Role
from apps.shop.models import Category, Product
from apps.cms.models import Page, ContactInfo, Testimonial
from decimal import Decimal
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Load initial data for DRY FRUITS DELIGHT application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load initial data...'))

        self.create_roles()
        self.create_users()
        self.create_categories()
        self.create_products()
        self.create_pages()
        self.create_contact_info()
        self.create_testimonials()

        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))

    def create_roles(self):
        self.stdout.write('Creating roles...')
        roles_data = [
            {'name': 'admin', 'description': 'Administrator with full access'},
            {'name': 'customer', 'description': 'Regular customer'},
            {'name': 'vendor', 'description': 'Product vendor'},
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            if created:
                self.stdout.write(f'  Created role: {role.name}')

    def create_users(self):
        self.stdout.write('Creating users...')
        admin_role = Role.objects.get(name='admin')
        customer_role = Role.objects.get(name='customer')

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dryfruitsdelight.com',
                'full_name': 'Admin User',
                'mobile': '+1234567890',
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('  Created admin user (username: admin, password: admin123)')

        customer, created = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@example.com',
                'full_name': 'John Doe',
                'mobile': '+1234567891',
                'role': customer_role,
            }
        )
        if created:
            customer.set_password('customer123')
            customer.save()
            self.stdout.write('  Created customer user (username: customer, password: customer123)')

    def create_categories(self):
        self.stdout.write('Creating categories...')
        categories_data = [
            {
                'name': 'Premium Nuts',
                'description': 'High-quality nuts sourced from the finest farms',
                'image_url': 'https://images.pexels.com/photos/1295572/pexels-photo-1295572.jpeg'
            },
            {
                'name': 'Dried Fruits',
                'description': 'Naturally dried fruits packed with nutrients',
                'image_url': 'https://images.pexels.com/photos/5617/food-salad-healthy-vegetables.jpg'
            },
            {
                'name': 'Seeds & Berries',
                'description': 'Nutritious seeds and antioxidant-rich berries',
                'image_url': 'https://images.pexels.com/photos/1556665/pexels-photo-1556665.jpeg'
            },
            {
                'name': 'Gift Boxes',
                'description': 'Curated gift boxes for special occasions',
                'image_url': 'https://images.pexels.com/photos/264869/pexels-photo-264869.jpeg'
            },
            {
                'name': 'Organic Collection',
                'description': 'Certified organic dry fruits and nuts',
                'image_url': 'https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg'
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  Created category: {category.name}')

    def create_products(self):
        self.stdout.write('Creating products...')

        categories = {cat.name: cat for cat in Category.objects.all()}

        products_data = [
            {
                'name': 'Premium Almonds',
                'category': 'Premium Nuts',
                'description': 'High-quality California almonds, rich in vitamin E and healthy fats. Perfect for snacking or adding to recipes.',
                'price': Decimal('12.99'),
                'stock_quantity': 100,
                'image_url': 'https://images.pexels.com/photos/1295572/pexels-photo-1295572.jpeg',
                'nutritional_info': 'Per 100g: Calories 579, Protein 21g, Fat 49g, Carbs 22g',
            },
            {
                'name': 'Organic Cashews',
                'category': 'Premium Nuts',
                'description': 'Creamy organic cashews from sustainable farms. Excellent source of copper and magnesium.',
                'price': Decimal('15.99'),
                'stock_quantity': 80,
                'image_url': 'https://images.pexels.com/photos/1295572/pexels-photo-1295572.jpeg',
                'nutritional_info': 'Per 100g: Calories 553, Protein 18g, Fat 44g, Carbs 30g',
            },
            {
                'name': 'Walnut Halves',
                'category': 'Premium Nuts',
                'description': 'Premium walnut halves packed with omega-3 fatty acids and antioxidants.',
                'price': Decimal('18.99'),
                'stock_quantity': 60,
                'image_url': 'https://images.pexels.com/photos/1295572/pexels-photo-1295572.jpeg',
                'nutritional_info': 'Per 100g: Calories 654, Protein 15g, Fat 65g, Carbs 14g',
            },
            {
                'name': 'Turkish Apricots',
                'category': 'Dried Fruits',
                'description': 'Sun-dried Turkish apricots, naturally sweet and rich in fiber and vitamins.',
                'price': Decimal('9.99'),
                'stock_quantity': 120,
                'image_url': 'https://images.pexels.com/photos/5617/food-salad-healthy-vegetables.jpg',
                'nutritional_info': 'Per 100g: Calories 241, Protein 3g, Fat 0.5g, Carbs 63g',
            },
            {
                'name': 'Medjool Dates',
                'category': 'Dried Fruits',
                'description': 'Premium Medjool dates from Jordan. Natural sweetener and energy booster.',
                'price': Decimal('13.99'),
                'stock_quantity': 90,
                'image_url': 'https://images.pexels.com/photos/5617/food-salad-healthy-vegetables.jpg',
                'nutritional_info': 'Per 100g: Calories 277, Protein 2g, Fat 0.2g, Carbs 75g',
            },
            {
                'name': 'Golden Raisins',
                'category': 'Dried Fruits',
                'description': 'Sweet golden raisins, perfect for baking or snacking. High in iron and potassium.',
                'price': Decimal('7.99'),
                'stock_quantity': 150,
                'image_url': 'https://images.pexels.com/photos/5617/food-salad-healthy-vegetables.jpg',
                'nutritional_info': 'Per 100g: Calories 299, Protein 3g, Fat 0.5g, Carbs 79g',
            },
            {
                'name': 'Chia Seeds',
                'category': 'Seeds & Berries',
                'description': 'Organic chia seeds loaded with omega-3s, fiber, and protein.',
                'price': Decimal('11.99'),
                'stock_quantity': 100,
                'image_url': 'https://images.pexels.com/photos/1556665/pexels-photo-1556665.jpeg',
                'nutritional_info': 'Per 100g: Calories 486, Protein 17g, Fat 31g, Carbs 42g',
            },
            {
                'name': 'Goji Berries',
                'category': 'Seeds & Berries',
                'description': 'Himalayan goji berries rich in antioxidants and vitamin C.',
                'price': Decimal('16.99'),
                'stock_quantity': 70,
                'image_url': 'https://images.pexels.com/photos/1556665/pexels-photo-1556665.jpeg',
                'nutritional_info': 'Per 100g: Calories 349, Protein 14g, Fat 0.4g, Carbs 77g',
            },
            {
                'name': 'Premium Gift Box',
                'category': 'Gift Boxes',
                'description': 'Elegant gift box containing a selection of our finest nuts and dried fruits.',
                'price': Decimal('49.99'),
                'stock_quantity': 40,
                'image_url': 'https://images.pexels.com/photos/264869/pexels-photo-264869.jpeg',
                'nutritional_info': 'Variety pack',
            },
            {
                'name': 'Organic Mixed Nuts',
                'category': 'Organic Collection',
                'description': 'Certified organic mixed nuts including almonds, cashews, and walnuts.',
                'price': Decimal('19.99'),
                'stock_quantity': 85,
                'image_url': 'https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg',
                'nutritional_info': 'Per 100g: Calories 600, Protein 18g, Fat 50g, Carbs 25g',
            },
        ]

        for prod_data in products_data:
            category = categories.get(prod_data['category'])
            product_slug = slugify(prod_data['name'])
            if category:
                product, created = Product.objects.get_or_create(
                slug=product_slug,
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock_quantity'],
                    'nutritional_info': prod_data.get('nutritional_info', ''),
                    'is_active': True,
                    'is_featured': False,
                }
            )
            if created:
                self.stdout.write(f'  Created product: {product.name}')
            else:
                self.stdout.write(f'  Product already exists: {product.name}')

    def create_pages(self):
        self.stdout.write('Creating CMS pages...')

        pages_data = [
            {
                'page_type': 'about',
                'title': 'About DRY FRUITS DELIGHT',
                'content': '''
                    <h2>Our Story</h2>
                    <p>DRY FRUITS DELIGHT was founded with a simple mission: to bring the finest quality dry fruits and nuts from around the world directly to your doorstep. We believe in the power of natural, wholesome nutrition and the incredible benefits that premium nuts and dried fruits can bring to your daily life.</p>

                    <h3>Our Values</h3>
                    <ul>
                        <li><strong>Quality First:</strong> We source only the highest quality products from trusted farms worldwide.</li>
                        <li><strong>Sustainability:</strong> We are committed to sustainable farming practices and ethical sourcing.</li>
                        <li><strong>Customer Satisfaction:</strong> Your health and happiness are our top priorities.</li>
                        <li><strong>Transparency:</strong> We believe in complete transparency about our products and sourcing.</li>
                    </ul>

                    <h3>What Makes Us Different</h3>
                    <p>Every product we offer is carefully selected and tested to ensure it meets our rigorous quality standards. We work directly with farmers and cooperatives who share our commitment to quality and sustainability. Our products are free from artificial additives, preservatives, and harmful chemicals.</p>

                    <p>We believe in providing not just products, but a complete experience of health and wellness. From our carefully curated selection to our thoughtful packaging, every detail is designed with your well-being in mind.</p>
                ''',
                'meta_description': 'Learn about DRY FRUITS DELIGHT, your trusted source for premium dry fruits and nuts.',
            },
            {
                'page_type': 'contact',
                'title': 'Contact Us',
                'content': '''
                    <h2>Get In Touch</h2>
                    <p>We'd love to hear from you! Whether you have questions about our products, need help with an order, or just want to say hello, our team is here to help.</p>

                    <h3>Customer Service</h3>
                    <p><strong>Phone:</strong> +91-8309232756<br>
                    <strong>Email:</strong> info@dryfruitsdelight.com<br>
                    <strong>WhatsApp:</strong> +91-8309232756</p>

                    <h3>Business Hours</h3>
                    <p>Monday - Friday: 9:00 AM - 6:00 PM<br>
                    Saturday: 10:00 AM - 4:00 PM<br>
                    Sunday: Closed</p>

                    <h3>Visit Our Store</h3>
                    <p>Shop no 4 , QMAKS Ayzal Residency , S.A. Colony , Tolichowki, Hyderabad -500008<br>
                    Hyderabad -500008<br>
                </p>

                    <h3>Follow Us</h3>
                    <p>Stay connected with us on social media for the latest updates, recipes, and special offers.</p>
                ''',
                'meta_description': 'Contact DRY FRUITS DELIGHT customer service team. We are here to help!',
            },
            {
                'page_type': 'shipping',
                'title': 'Shipping Policy',
                'content': '''
                    <h2>Shipping Information</h2>

                    <h3>Shipping Methods</h3>
                    <p>We offer several shipping options to meet your needs:</p>
                    <ul>
                        <li><strong>Standard Shipping:</strong> 5-7 business days - Free on orders over ₹50</li>
                        <li><strong>Express Shipping:</strong> 2-3 business days - ₹9.99</li>
                        <li><strong>Overnight Shipping:</strong> 1 business day - ₹19.99</li>
                    </ul>

                    <h3>Processing Time</h3>
                    <p>Orders are typically processed within 1-2 business days. You will receive a confirmation email with tracking information once your order ships.</p>

                    <h3>International Shipping</h3>
                    <p>We currently ship to select international destinations. Shipping costs and delivery times vary by location. Please contact us for specific rates and availability.</p>

                    <h3>Package Protection</h3>
                    <p>All orders are carefully packaged to ensure your products arrive fresh and in perfect condition. We use eco-friendly packaging materials whenever possible.</p>

                    <h3>Tracking Your Order</h3>
                    <p>Once your order ships, you'll receive a tracking number via email. You can also track your order by logging into your account dashboard.</p>
                ''',
                'meta_description': 'Learn about DRY FRUITS DELIGHT shipping options, delivery times, and policies.',
            },
            {
                'page_type': 'returns',
                'title': 'Returns & Refunds',
                'content': '''
                    <h2>Return Policy</h2>
                    <p>We want you to be completely satisfied with your purchase. If you're not happy with your order for any reason, we're here to help.</p>

                    <h3>30-Day Return Policy</h3>
                    <p>You may return most items within 30 days of delivery for a full refund. Products must be unopened and in their original packaging.</p>

                    <h3>How to Return an Item</h3>
                    <ol>
                        <li>Contact our customer service team at info@dryfruitsdelight.com</li>
                        <li>Provide your order number and reason for return</li>
                        <li>We'll provide you with a return shipping label</li>
                        <li>Pack the item securely and ship it back to us</li>
                        <li>Once received, we'll process your refund within 5-7 business days</li>
                    </ol>

                    <h3>Refund Method</h3>
                    <p>Refunds will be issued to your original payment method. Please allow 5-10 business days for the refund to appear in your account.</p>

                    <h3>Damaged or Defective Items</h3>
                    <p>If you receive a damaged or defective product, please contact us immediately. We'll arrange for a replacement or full refund at no additional cost to you.</p>

                    <h3>Non-Returnable Items</h3>
                    <p>For health and safety reasons, opened food products cannot be returned unless defective or damaged.</p>
                ''',
                'meta_description': 'DRY FRUITS DELIGHT return and refund policy. Learn about our hassle-free returns process.',
            },
            {
                'page_type': 'terms',
                'title': 'Terms & Conditions',
                'content': '''
                    <h2>Terms of Service</h2>
                    <p><em>Last updated: January 2024</em></p>

                    <h3>Agreement to Terms</h3>
                    <p>By accessing and using DRY FRUITS DELIGHT's website and services, you agree to be bound by these Terms and Conditions. If you do not agree with any part of these terms, please do not use our services.</p>

                    <h3>Use of Service</h3>
                    <p>You must be at least 18 years old to make purchases on our website. You agree to provide accurate, current, and complete information during the registration and purchasing process.</p>

                    <h3>Product Information</h3>
                    <p>We strive to provide accurate product descriptions and pricing. However, we do not warrant that product descriptions, pricing, or other content is accurate, complete, reliable, current, or error-free.</p>

                    <h3>Orders and Payment</h3>
                    <p>All orders are subject to acceptance and availability. We reserve the right to refuse or cancel any order for any reason. Payment must be received before order processing.</p>

                    <h3>Intellectual Property</h3>
                    <p>All content on this website, including text, graphics, logos, images, and software, is the property of DRY FRUITS DELIGHT and protected by copyright laws.</p>

                    <h3>Limitation of Liability</h3>
                    <p>DRY FRUITS DELIGHT shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of our services.</p>

                    <h3>Changes to Terms</h3>
                    <p>We reserve the right to modify these terms at any time. Your continued use of the service after changes constitutes acceptance of the new terms.</p>

                    <h3>Contact Information</h3>
                    <p>For questions about these Terms and Conditions, please contact us at info@dryfruitsdelight.com</p>
                ''',
                'meta_description': 'Read DRY FRUITS DELIGHT Terms and Conditions for using our website and services.',
            },
            {
                'page_type': 'privacy',
                'title': 'Privacy Policy',
                'content': '''
                    <h2>Privacy Policy</h2>
                    <p><em>Last updated: January 2024</em></p>

                    <h3>Information We Collect</h3>
                    <p>We collect information that you provide directly to us, including:</p>
                    <ul>
                        <li>Name, email address, and phone number</li>
                        <li>Shipping and billing addresses</li>
                        <li>Payment information</li>
                        <li>Order history and preferences</li>
                        <li>Communications with our customer service team</li>
                    </ul>

                    <h3>How We Use Your Information</h3>
                    <p>We use the information we collect to:</p>
                    <ul>
                        <li>Process and fulfill your orders</li>
                        <li>Communicate with you about your orders and account</li>
                        <li>Send you promotional materials (with your consent)</li>
                        <li>Improve our products and services</li>
                        <li>Prevent fraud and enhance security</li>
                    </ul>

                    <h3>Information Sharing</h3>
                    <p>We do not sell or rent your personal information to third parties. We may share your information with:</p>
                    <ul>
                        <li>Service providers who assist in our operations</li>
                        <li>Payment processors for transaction processing</li>
                        <li>Shipping companies for order delivery</li>
                        <li>Legal authorities when required by law</li>
                    </ul>

                    <h3>Data Security</h3>
                    <p>We implement appropriate security measures to protect your personal information. However, no method of transmission over the internet is 100% secure.</p>

                    <h3>Your Rights</h3>
                    <p>You have the right to:</p>
                    <ul>
                        <li>Access your personal information</li>
                        <li>Correct inaccurate information</li>
                        <li>Request deletion of your information</li>
                        <li>Opt-out of marketing communications</li>
                    </ul>

                    <h3>Cookies</h3>
                    <p>We use cookies to enhance your browsing experience and analyze website traffic. You can control cookies through your browser settings.</p>

                    <h3>Changes to Privacy Policy</h3>
                    <p>We may update this Privacy Policy from time to time. We will notify you of any significant changes by email or through our website.</p>

                    <h3>Contact Us</h3>
                    <p>If you have questions about this Privacy Policy, please contact us at privacy@dryfruitsdelight.com</p>
                ''',
                'meta_description': 'Learn how DRY FRUITS DELIGHT collects, uses, and protects your personal information.',
            },
        ]

        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                page_type=page_data['page_type'],
                defaults={
                    'title': page_data['title'],
                    'content': page_data['content'],
                    'meta_description': page_data['meta_description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'  Created page: {page.title}')

    def create_contact_info(self):
        self.stdout.write('Creating contact information...')

        contact_info, created = ContactInfo.objects.get_or_create(
            id=1,
            defaults={
                'business_name': 'DRY FRUITS DELIGHT',
                'tagline': 'Premium Dry Fruits & Nuts',
                'email': 'info@dryfruitsdelight.com',
                'phone': '+91-8309232756',
                'whatsapp': '+91-8309232756',
                'address': 'Shop no 4 , QMAKS Ayzal Residency , S.A. Colony , Tolichowki, Hyderabad -500008',
                'city': 'Hyderabad -500008',
                'pincode': '12345',
                'facebook_url': 'https://facebook.com/dryfruitsdelight',
                'instagram_url': 'https://instagram.com/dryfruitsdelight',
                'twitter_url': 'https://twitter.com/dryfruitsdelight',
                'youtube_url': 'https://youtube.com/dryfruitsdelight',
                'business_hours': 'Monday - Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM\nSunday: Closed',
            }
        )
        if created:
            self.stdout.write('  Created contact information')

    def create_testimonials(self):
        self.stdout.write('Creating testimonials...')

        testimonials_data = [
            {
                'customer_name': 'Sarah Johnson',
                'rating': 5,
                'comment': 'The quality of the almonds I received was outstanding! Fresh, crunchy, and perfectly packaged. DRY FRUITS DELIGHT has become my go-to source for all my nut needs.',
                'location': 'New York, NY',
            },
            {
                'customer_name': 'Michael Chen',
                'rating': 5,
                'comment': 'I\'ve been ordering from DRY FRUITS DELIGHT for over a year now. Their organic cashews are the best I\'ve ever tasted, and the customer service is exceptional.',
                'location': 'San Francisco, CA',
            },
            {
                'customer_name': 'Emily Rodriguez',
                'rating': 5,
                'comment': 'Love the variety and quality! The gift box I ordered was beautifully presented and made a perfect gift. The recipient was thrilled!',
                'location': 'Austin, TX',
            },
            {
                'customer_name': 'David Thompson',
                'rating': 4,
                'comment': 'Great selection of products and fast shipping. The Turkish apricots are delicious and perfect for my morning oatmeal.',
                'location': 'Seattle, WA',
            },
            {
                'customer_name': 'Lisa Patel',
                'rating': 5,
                'comment': 'As someone who values organic and sustainable products, DRY FRUITS DELIGHT is perfect. The quality is excellent and I appreciate their commitment to ethical sourcing.',
                'location': 'Portland, OR',
            },
            {
                'customer_name': 'James Wilson',
                'rating': 5,
                'comment': 'The best walnuts I\'ve ever purchased! They arrived fresh and well-packaged. I\'ve already placed my second order.',
                'location': 'Boston, MA',
            },
        ]

        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                customer_name=test_data['customer_name'],
                defaults={
                    'rating': test_data['rating'],
                    'comment': test_data['comment'],
                    'location': test_data.get('location', ''),
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'  Created testimonial from: {testimonial.customer_name}')
