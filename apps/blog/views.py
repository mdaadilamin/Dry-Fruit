from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Post, Category, Comment

def blog_home(request):
    """Display all published blog posts"""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get featured posts
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:3]
    
    # Get categories with post counts
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'page_obj': page_obj,
        'featured_posts': featured_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    """Display a single blog post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Get related posts from the same category
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    # Get categories with post counts
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'categories': categories,
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    """Display posts from a specific category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    posts = Post.objects.filter(category=category, status='published').select_related('author')
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with post counts
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/category_posts.html', context)

def search_posts(request):
    """Search blog posts"""
    query = request.GET.get('q', '')
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query)
        ).filter(status='published').select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with post counts
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/search_results.html', context)