from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Category
from apps.users.models import Role

User = get_user_model()

class CategoryManagementTestCase(TestCase):
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
        
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
    
    def test_category_list_view(self):
        """Test that the category management page loads correctly"""
        response = self.client.get(reverse('shop:category_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category Management')
        self.assertContains(response, self.category.name)
    
    def test_add_category(self):
        """Test adding a new category"""
        response = self.client.post(reverse('shop:category_management'), {
            'action': 'add',
            'name': 'New Category',
            'description': 'New category description',
            'is_active': 'on'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Category.objects.filter(name='New Category').exists())
    
    def test_edit_category(self):
        """Test editing an existing category"""
        response = self.client.post(reverse('shop:category_management'), {
            'action': 'edit',
            'id': self.category.id,
            'name': 'Updated Category',
            'description': 'Updated description',
            'is_active': 'on'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')
        self.assertEqual(self.category.description, 'Updated description')
    
    def test_delete_category(self):
        """Test deleting a category"""
        response = self.client.post(reverse('shop:category_management'), {
            'action': 'delete',
            'id': self.category.id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())