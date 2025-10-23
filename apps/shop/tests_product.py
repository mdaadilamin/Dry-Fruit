from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from .models import Product, Category
from apps.users.models import Role

User = get_user_model()

class ProductManagementTestCase(TestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name='admin', description='Administrator')
        self.employee_role = Role.objects.create(name='employee', description='Employee')
        
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
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            slug=slugify('Test Product'),
            category=self.category,
            description='Test product description',
            price=10.99,
            stock=100
        )
        
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
    
    def test_product_list_view(self):
        """Test that the product management page loads correctly"""
        response = self.client.get(reverse('shop:product_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product Management')
        self.assertContains(response, self.product.name)
    
    def test_add_product(self):
        """Test adding a new product"""
        response = self.client.post(reverse('shop:product_add'), {
            'name': 'New Product',
            'category': self.category.id,
            'price': '15.99',
            'stock': 50,
            'description': 'New product description',
            'is_active': 'on'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Product.objects.filter(name='New Product').exists())
    
    def test_edit_product(self):
        """Test editing an existing product"""
        response = self.client.post(reverse('shop:product_edit', args=[self.product.id]), {
            'name': 'Updated Product',
            'category': self.category.id,
            'price': '19.99',
            'stock': 75,
            'description': 'Updated product description',
            'is_active': 'on'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(float(self.product.price), 19.99)
        self.assertEqual(self.product.stock, 75)
    
    def test_product_detail_view(self):
        """Test that the product detail page loads correctly"""
        response = self.client.get(reverse('core:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)