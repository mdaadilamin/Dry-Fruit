# Utility Functions Documentation

This document provides documentation for the utility functions created to improve code reusability and maintainability in the NutriHarvest e-commerce platform.

## Core Utilities

### `get_related_products(product, limit=4)`

**Description**: Retrieves a list of related products based on category, tags, and purchase history.

**Parameters**:
- `product` (Product): The product for which to find related products
- `limit` (int, optional): Maximum number of related products to return (default: 4)

**Returns**: List of Product objects

**Logic**:
1. Finds products in the same category
2. If the product has tags, also finds products with similar tags
3. Identifies products frequently bought together based on order history
4. Combines all results and returns up to `limit` products

**Usage**:
```python
from apps.core.utils import get_related_products

related_products = get_related_products(product, limit=6)
```

### `get_upsell_products(product, limit=4)`

**Description**: Retrieves a list of upsell products (higher priced or premium versions) from the same category.

**Parameters**:
- `product` (Product): The product for which to find upsell products
- `limit` (int, optional): Maximum number of upsell products to return (default: 4)

**Returns**: List of Product objects

**Logic**:
1. Finds products in the same category with higher price
2. Includes products tagged as 'premium' or 'deluxe'
3. Orders results by price and returns up to `limit` products

**Usage**:
```python
from apps.core.utils import get_upsell_products

upsell_products = get_upsell_products(product, limit=3)
```

### `get_product_rating_stats(product)`

**Description**: Calculates rating statistics for a product including average rating and review count.

**Parameters**:
- `product` (Product): The product for which to calculate rating statistics

**Returns**: Dictionary with keys:
- `avg_rating` (float): Average rating for the product
- `review_count` (int): Total number of reviews for the product

**Usage**:
```python
from apps.core.utils import get_product_rating_stats

rating_stats = get_product_rating_stats(product)
print(f"Average rating: {rating_stats['avg_rating']}")
print(f"Review count: {rating_stats['review_count']}")
```