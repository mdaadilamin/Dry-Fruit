from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.users.models import Role

User = get_user_model()

class AdminPanelTestCase(TestCase):
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
        
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
    
    def test_admin_panel_access(self):
        """Test that the admin panel page loads correctly"""
        response = self.client.get(reverse('core:admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
    
    def test_product_management_link_exists(self):
        """Test that the product management link exists in the admin panel"""
        response = self.client.get(reverse('core:admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Products')
        self.assertContains(response, reverse('shop:product_management'))
    
    def test_category_management_link_exists(self):
        """Test that the category management link exists in the admin panel"""
        response = self.client.get(reverse('core:admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Categories')
        self.assertContains(response, reverse('shop:category_management'))