from django.db import models
from django.utils import timezone
from django.urls import reverse
from apps.users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    excerpt = models.TextField(max_length=300, blank=True, help_text='Brief summary of the post')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords for SEO")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['post']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author_name} on {self.post}'