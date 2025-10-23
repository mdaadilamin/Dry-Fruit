from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.shop.models import Product, Category
from apps.users.models import Role
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ImageHandlingTestCase(TestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name='admin', description='Administrator')
        
        # Create a test user with admin privileges
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            full_name='Admin User',
            role=self.admin_role
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        
        # Create a test product without image
        self.product_without_image = Product.objects.create(
            name='Product Without Image',
            slug='product-without-image',
            category=self.category,
            description='Test product without image',
            price=10.99,
            stock=100
        )
        
        # Create a test product with image
        image_content = b"fake image content"
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        
        self.product_with_image = Product.objects.create(
            name='Product With Image',
            slug='product-with-image',
            category=self.category,
            description='Test product with image',
            price=15.99,
            stock=50,
            image=test_image
        )
        
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
    
    def test_product_management_displays_images(self):
        """Test that the product management page displays images correctly"""
        response = self.client.get(reverse('shop:product_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product Management')
        # Check that both products are displayed
        self.assertContains(response, self.product_without_image.name)
        self.assertContains(response, self.product_with_image.name)
    
    def test_product_detail_displays_placeholder_for_missing_image(self):
        """Test that product detail page uses placeholder for products without images"""
        response = self.client.get(reverse('core:product_detail', args=[self.product_without_image.id]))
        self.assertEqual(response.status_code, 200)
        # Check that the placeholder image is used
        self.assertContains(response, 'static/images/placeholder.jpg')
    
    def test_product_detail_displays_image_for_product_with_image(self):
        """Test that product detail page displays actual image for products with images"""
        response = self.client.get(reverse('core:product_detail', args=[self.product_with_image.id]))
        self.assertEqual(response.status_code, 200)
        # Check that the product image is displayed
        self.assertContains(response, self.product_with_image.image.url)
    
    def test_shop_page_displays_images_correctly(self):
        """Test that the shop page displays images correctly"""
        response = self.client.get(reverse('core:shop'))
        self.assertEqual(response.status_code, 200)
        # Check that both products are displayed with appropriate images
        self.assertContains(response, self.product_without_image.name)
        self.assertContains(response, self.product_with_image.name)