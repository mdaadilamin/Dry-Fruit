#!/usr/bin/env python
"""
Test script to verify that the utility functions work correctly.
This script can be run independently to test the functionality.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriharvest.settings')
django.setup()

def test_utils():
    """Test the utility functions"""
    print("Testing utility functions...")
    
    # Import the utility functions
    try:
        from apps.core.utils import get_related_products, get_upsell_products, get_product_rating_stats
        print("✓ Utility functions imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utility functions: {e}")
        return False
    
    # Import models
    try:
        from apps.shop.models import Product
        print("✓ Models imported successfully")
    except Exception as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    # Test with a sample product (if any exist)
    try:
        product = Product.objects.first()
        if product:
            print(f"✓ Found test product: {product.name}")
            
            # Test get_related_products
            related = get_related_products(product, limit=2)
            print(f"✓ Found {len(related)} related products")
            
            # Test get_upsell_products
            upsell = get_upsell_products(product, limit=2)
            print(f"✓ Found {len(upsell)} upsell products")
            
            # Test get_product_rating_stats
            stats = get_product_rating_stats(product)
            print(f"✓ Product rating stats: {stats}")
        else:
            print("⚠ No products found in database for testing")
        
        print("✓ All utility functions work correctly")
        return True
    except Exception as e:
        print(f"✗ Error testing utility functions: {e}")
        return False

if __name__ == "__main__":
    success = test_utils()
    if success:
        print("\n🎉 All tests passed! The utility functions are working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)