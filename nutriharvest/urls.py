from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticViewSitemap, ProductSitemap, CategorySitemap, BlogPostSitemap, CMSPagesSitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/shop/', include('apps.shop.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/cms/', include('apps.cms.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('payments/', include('payments.urls')),
    path('blog/', include('apps.blog.urls')),
    path('', include('apps.core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {
        'static': StaticViewSitemap,
        'products': ProductSitemap,
        'categories': CategorySitemap,
        'blog': BlogPostSitemap,
        'cms': CMSPagesSitemap,
    }}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)