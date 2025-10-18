from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.shop.models import Product, Category
from apps.blog.models import Post
from apps.cms.models import Page

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['core:home', 'core:shop', 'core:chocolates_category', 'core:spices_category', 
                'blog:home', 'cms:page_view']

    def location(self, item):
        if item == 'cms:page_view':
            # For CMS pages, we need to provide specific page types
            # We'll handle this separately
            return ''
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(is_active=True)

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

# Custom sitemap for CMS pages with specific page types
class CMSPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['about', 'contact', 'privacy', 'terms', 'shipping', 'returns']

    def location(self, item):
        return reverse('cms:page_view', kwargs={'page_type': item})