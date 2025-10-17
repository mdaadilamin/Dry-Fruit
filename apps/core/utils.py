from django.db.models import Avg, Count, Q, Sum
from apps.shop.models import Product, ProductReview
from apps.orders.models import OrderItem

def get_related_products(product, limit=4):
    """Get related products based on category, tags, and purchase history"""
    # Start with products from the same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)
    
    # If product has tags, also look for products with similar tags
    if product.tags:
        tag_list = [tag.strip() for tag in product.tags.split(',')]
        tag_queries = Q()
        for tag in tag_list:
            tag_queries = tag_queries | Q(tags__icontains=tag)
        
        # Get products with similar tags
        tagged_products = Product.objects.filter(
            tag_queries,
            is_active=True
        ).exclude(id=product.id).distinct()
        
        # Combine category and tagged products
        related_products = related_products.union(tagged_products)
    
    # Get products that are frequently bought together (purchase history)
    # Find orders that contain this product
    orders_with_product = OrderItem.objects.filter(product=product).values_list('order_id', flat=True)
    
    # Find other products in those orders
    if orders_with_product.exists():
        frequently_bought_together = Product.objects.filter(
            orderitem__order_id__in=orders_with_product,
            is_active=True
        ).exclude(id=product.id).annotate(
            purchase_count=Count('orderitem')
        ).order_by('-purchase_count')
        
        # Combine with existing related products
        related_products = related_products.union(frequently_bought_together)
    
    # Convert to list and limit
    related_products_list = list(related_products[:limit*2])  # Get more to ensure we have enough after filtering
    
    # Remove the current product if it's in the list
    related_products_list = [p for p in related_products_list if p.id != product.id]
    
    # Return limited results
    return related_products_list[:limit]

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