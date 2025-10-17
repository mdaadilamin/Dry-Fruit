# NutriHarvest - Complete Django E-commerce Application

A comprehensive, production-ready Django e-commerce platform for a premium dry fruit shop with advanced features including role-based access control, order management, content management system, and enhanced user experience with notifications and improved navigation.

## 🚀 Features

### Recent Enhancements
- **Enhanced Navigation**: Added product categories dropdown with Dry Fruits, Gift Boxes, Chocolates, and Spices
- **Blog Integration**: Added blog link to main navigation
- **Product Search**: Implemented search bar in navbar for quick product discovery
- **Notification System**: Added pop-up notifications for promotions and new arrivals
- **Notification Bell**: Added notification icon in navbar with unread count and dropdown preview

### Frontend Features
- **Responsive Design**: Mobile-first design with Bootstrap 5
- **Product Catalog**: Advanced search, filtering, and sorting
- **Shopping Cart**: Add/remove items with real-time updates  
- **User Authentication**: Registration, login, password reset
- **Customer Dashboard**: Order history, profile management
- **Rich UI/UX**: Premium "Rich Earthy Luxury" theme

### Backend Features
- **Django REST Framework**: Full API support
- **Role-Based Access Control**: Admin, Employee, Customer roles
- **Product Management**: CRUD operations with categories
- **Order Management**: Complete order lifecycle management
- **Content Management**: Banners, testimonials, pages
- **Email Notifications**: Automated order confirmations
- **Activity Logging**: Complete audit trail

### Admin Features
- **Comprehensive Dashboard**: Sales analytics and metrics
- **User Management**: Employee and customer management
- **Permission System**: Granular access control
- **Inventory Management**: Stock tracking and alerts
- **Report Generation**: Sales and inventory reports
- **CMS**: Manage website content dynamically
- **Notification Management**: Create and manage system notifications
- **Enhanced Navigation**: Improved admin navigation and menu structure

## 🛠️ Tech Stack

- **Backend**: Django 5.2.7, Django REST Framework
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Authentication**: Django built-in authentication
- **File Storage**: Django file handling with Pillow
- **Email**: Django email backend (configurable)
- **Icons**: Lucide Icons for consistent iconography

## 📋 Requirements

- Python 3.13.7
- Django 5.2.7
- Node.js (for frontend assets)
- MySQL (for production)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd nutriharvest
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note**: The project has been upgraded to Django 5.2.7 to resolve dependency conflicts with django-filter 25.2.

### 4. Environment Configuration
Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
```

Edit `.env` with your database and email settings:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Sample Data
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
python manage.py collectstatic
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🎯 Default Login Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator (Full Access)

### Employee Account  
- **Username**: employee
- **Password**: employee123
- **Role**: Sales Executive (Limited Access)

### Customer Account
- **Username**: customer
- **Password**: customer123
- **Role**: Customer (Frontend Only)

> **Note**: After logging in as admin, you can manage system notifications through the admin panel under the Notifications section.

## 📁 Project Structure

```
nutriharvest/
├── apps/
│   ├── core/           # Main app with views and URLs
│   ├── users/          # User management and authentication
│   ├── shop/           # Product and category management
│   ├── orders/         # Cart and order management
│   ├── cms/            # Content management system
│   └── notifications/  # Email, SMS, and system notifications
├── templates/          # HTML templates
├── static/            # CSS, JS, and image files
├── media/             # Uploaded files
├── fixtures/          # Sample data
└── nutriharvest/      # Django project settings
```

## 🔐 User Roles & Permissions

### Administrator
- Full system access
- Manage all users, products, orders
- Access to reports and analytics
- Content management privileges

### Employee (Sales Executive)
- Product management
- Order processing
- Customer support
- Limited administrative access

### Customer
- Browse and purchase products
- Manage personal profile
- Track order history
- Shopping cart functionality

## 🛒 E-commerce Features

### Product Management
- Categories with hierarchical structure
- Product variants and images
- Inventory tracking
- SEO-friendly URLs
- Bulk operations

### Order Processing
- Shopping cart with session storage
- Multiple payment methods (COD, Online)
- Order status tracking
- Email notifications
- Invoice generation

### Customer Experience
- Advanced product search and filtering
- Wishlist functionality
- Product reviews and ratings
- Responsive design for mobile
- Fast checkout process
- Enhanced navigation with product categories dropdown
- Blog access from main navigation
- Real-time notification system

## 📧 Email & Notifications

### Email Templates
- Order confirmation
- Shipping updates
- Welcome emails
- Password reset

### SMS Integration (Ready)
- Order confirmations
- Delivery updates
- OTP verification
- Custom templates

### WhatsApp Integration (Ready)
- Order notifications
- Customer support
- Marketing messages
- Business API integration

### Notification System
- **System Notifications**: Admin-managed notifications for promotions, new arrivals, and announcements
- **User Notifications**: Personal notifications for order updates and account activities
- **Real-time Updates**: Automatic notification fetching with periodic updates
- **Notification Bell**: Navbar icon with unread count and dropdown preview
- **Pop-up Notifications**: Non-intrusive pop-ups for system-wide announcements

## 📊 Reports & Analytics

### Sales Reports
- Daily/Monthly/Yearly sales
- Product performance
- Customer analytics
- Revenue tracking

### Inventory Reports  
- Stock levels
- Low stock alerts
- Product movement
- Reorder recommendations

## 🚀 Production Deployment

### Database Configuration (MySQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nutriharvest_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Static Files Configuration
```python
STATIC_ROOT = '/path/to/static/files/'
MEDIA_ROOT = '/path/to/media/files/'
```

### Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📚 API Documentation

The application includes a comprehensive REST API:

### Endpoints
- `/api/shop/products/` - Product CRUD operations
- `/api/shop/categories/` - Category management
- `/api/orders/` - Order management
- `/api/users/` - User management
- `/api/cms/` - Content management
- `/api/notifications/system-notifications/` - System notifications
- `/api/notifications/user-notifications/` - User notifications

### Authentication
API uses session-based authentication with CSRF protection.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@nutriharvest.com or create an issue on GitHub.

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] AI-powered product recommendations
- [ ] Advanced inventory management
- [ ] Multi-vendor marketplace
- [ ] Subscription box service
- [ ] Loyalty program integration
- [ ] Advanced search with autocomplete
- [ ] Product comparison feature
- [ ] Wishlist sharing functionality

---

**NutriHarvest** - Premium Dry Fruits & Nuts E-commerce Platform
Built with ❤️ using Django and modern web technologies.