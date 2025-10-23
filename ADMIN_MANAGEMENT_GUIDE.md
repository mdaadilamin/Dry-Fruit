# Admin Management Guide

This document outlines all the management features available through the admin panel of the DRY FRUITS DELIGHT e-commerce platform.

## Accessing the Admin Panel

The admin panel can be accessed by administrators through the main navigation menu or by visiting:
- Main Dashboard: `/admin-panel/`
- Enhanced Dashboard: `/admin-panel/enhanced/`

## 1. Product Management

### URLs
- Product Management: `/shop/manage/products/`
- Add Product: `/shop/manage/products/add/`
- Edit Product: `/shop/manage/products/<product_id>/edit/`
- Category Management: `/shop/manage/categories/`

### Features
- View all products with pagination
- Add new products with detailed information (name, description, price, stock, etc.)
- Edit existing products
- Manage product categories
- Set featured products
- Apply discounts to products

## 2. Order Management

### URLs
- Order Management: `/orders/manage/`
- Order Details: `/orders/manage/<order_id>/`

### Features
- View all orders with filtering options
- Update order status (pending, processing, shipped, delivered, cancelled)
- View detailed order information
- Filter orders by status or customer

## 3. Customer Management

### URLs
- Customer List: `/users/customers/`
- Customer Details: `/users/customers/<customer_id>/`
- Edit Customer: `/users/customers/<customer_id>/edit/`

### Features
- View all customers
- View customer details and order history
- Edit customer information

## 4. Employee Management

### URLs
- Employee List: `/users/employees/`
- Employee Details: `/users/employees/<employee_id>/`
- Edit Employee: `/users/employees/<employee_id>/edit/`
- Create Employee: `/users/employees/create/`

### Features
- View all employees
- View employee details
- Edit employee information
- Create new employees

## 5. Blog Management

### URLs
- Post Management: `/blog/management/`
- Create Post: `/blog/create/`
- Edit Post: `/blog/edit/<post_id>/`
- Delete Post: `/blog/delete/<post_id>/`
- Category Management: `/blog/categories/`
- Create Category: `/blog/categories/create/`
- Edit Category: `/blog/categories/edit/<category_id>/`
- Comment Management: `/blog/comments/`
- Edit Comment: `/blog/comments/edit/<comment_id>/`

### Features
- Create, edit, and delete blog posts
- Manage blog categories
- Moderate comments (approve/reject)
- View all blog comments with filtering

## 6. Content Management (CMS)

### URLs
- Banner Management: `/cms/manage/banners/`
- Testimonial Management: `/cms/manage/testimonials/`
- Page Management: `/cms/manage/pages/`
- Contact Management: `/cms/manage/contact/`
- Enquiry Management: `/cms/manage/enquiries/`
- Newsletter Management: `/cms/manage/newsletter/`

### Features
- Manage website banners
- Manage customer testimonials
- Edit website pages (About, Contact, Privacy Policy, etc.)
- Update contact information
- View and resolve customer enquiries
- Manage newsletter subscribers

## 7. Marketing Management

### URLs
- Coupon Management: `/marketing/coupons/` or `/admin-panel/coupons/`

### Features
- Create, edit, and delete discount coupons
- Set coupon types (percentage, fixed amount, free shipping)
- Apply usage limits and expiration dates
- Target specific categories or products
- View coupon usage statistics

## 8. Notification Management

### URLs
- System Notifications: `/notifications/system-notifications/`

### Features
- Create and manage system notifications
- Set notification types (info, success, warning, error)
- Control visibility for users and guests
- Set expiration dates for notifications

## 9. Analytics and Reporting

### URLs
- Product Analytics: `/admin-panel/analytics/`

### Features
- View sales data and trends
- Monitor product performance
- Track inventory levels
- Analyze customer reviews and ratings
- View category performance metrics

## 10. User Roles and Permissions

### URLs
- Role Management: `/users/roles/manage/`
- Update Role Permissions: `/users/roles/<role_id>/permissions/`

### Features
- Manage user roles (admin, employee, customer)
- Set permissions for different roles
- Control access to various management features

## Quick Access from Admin Dashboard

The admin dashboard provides quick access buttons to all management sections:
- Products
- Categories
- Reviews
- Analytics
- Banners
- Testimonials
- Pages
- Newsletter
- Contact Info
- Enquiries
- Employees
- Customers
- Notifications
- Blog Posts
- Blog Categories
- Blog Comments
- Coupons
- Django Admin (for advanced management)

## System Status Monitoring

The admin panel also provides system status information:
- Server status
- Database connection
- Cache status
- Last backup time
- Storage usage

All management features are accessible through the admin panel, ensuring centralized control of the entire e-commerce platform.