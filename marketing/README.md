# Marketing Features for NutriHarvest

This document describes the marketing features implemented for the NutriHarvest e-commerce platform.

## Features Implemented

### 1. Coupon System
A comprehensive coupon system that allows administrators to create and manage various types of coupons:

- **Percentage Discount Coupons**: Apply a percentage discount to the cart total
- **Fixed Amount Discount Coupons**: Apply a fixed dollar amount discount to the cart total
- **Free Shipping Coupons**: Offer free shipping (currently displays discount but doesn't affect shipping costs)
- **Targeted Coupons**: Apply coupons to specific categories or products
- **Usage Limits**: Set maximum uses per coupon and per user
- **Time-based Validity**: Set start and end dates for coupons
- **Minimum Purchase Requirements**: Require a minimum cart amount to use coupons

### 2. Newsletter Subscription
Users can subscribe to the newsletter through the footer form. Subscriptions are stored in the database and can be managed through the admin interface.

### 3. SEO Enhancements
- Structured data (JSON-LD) for products and organization
- Improved meta tags for better search engine visibility
- Open Graph and Twitter card meta tags for social sharing
- Better URL structure and breadcrumb navigation

### 4. Admin Interface
- Coupon management interface for administrators
- View, create, edit, and delete coupons
- Track coupon usage statistics

## API Endpoints

### Apply Coupon
```
POST /api/marketing/coupon/apply/
Content-Type: application/json

{
    "coupon_code": "WELCOME10"
}
```

### Remove Coupon
```
POST /api/marketing/coupon/remove/
```

### Coupon Management
```
GET /api/marketing/coupons/
```

## Models

### Coupon
- `code`: Unique coupon code
- `coupon_type`: Type of discount (percentage, fixed, free_shipping)
- `discount_value`: Discount amount (percentage or fixed value)
- `discount_application`: Where the discount applies (cart, category, product)
- `category`: Target category (optional)
- `product`: Target product (optional)
- `max_uses`: Maximum total uses (optional)
- `used_count`: Number of times used
- `max_uses_per_user`: Maximum uses per user
- `is_active`: Whether the coupon is active
- `valid_from`: When the coupon becomes valid
- `valid_to`: When the coupon expires (optional)
- `min_purchase_amount`: Minimum cart amount required (optional)

### CouponUsage
- `coupon`: Reference to the coupon used
- `user`: User who used the coupon
- `order`: Order associated with the coupon usage (optional)
- `used_at`: When the coupon was used

## Usage

### For Customers
1. Add items to cart
2. Go to cart page
3. Enter coupon code in the coupon field
4. Click "Apply" to apply the discount
5. Proceed to checkout with discounted total

### For Administrators
1. Navigate to the admin panel
2. Go to Marketing > Coupons
3. Add, edit, or delete coupons as needed
4. View coupon usage statistics

## Future Enhancements
- Integration with email marketing platforms
- Advanced segmentation for targeted coupons
- A/B testing for marketing campaigns
- Referral program implementation
- Loyalty points system