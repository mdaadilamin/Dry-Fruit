from django.db.models import Avg, Count, Q, Sum
from apps.shop.models import Product, ProductReview
from apps.orders.models import OrderItem

def get_related_products(product, limit=4):
    """Get related products based on category, tags, and purchase history"""
    try:
        # Start with products from the same category
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:limit]
        
        return list(related_products)
    except Exception:
        # If there's any issue, return an empty list
        return []

def get_upsell_products(product, limit=4):
    """Get upsell products (higher priced or premium versions)"""
    # Get products from the same category with higher price or marked as premium
    upsell_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).filter(
        Q(price__gt=product.price) | Q(tags__icontains='premium') | Q(tags__icontains='deluxe')
    ).order_by('price')[:limit]
    
    return list(upsell_products)

def get_product_rating_stats(product):
    """Get rating statistics for a product"""
    reviews = ProductReview.objects.filter(product=product)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()
    
    return {
        'avg_rating': avg_rating,
        'review_count': review_count
    }