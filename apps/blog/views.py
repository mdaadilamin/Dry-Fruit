from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from apps.blog.models import Post, Category, Comment
from .forms import PostForm, CategoryForm, CommentForm
import operator
from functools import reduce

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
    
    # Process keywords into a list
    keywords_list = []
    if post.keywords:
        keywords_list = [keyword.strip() for keyword in post.keywords.split(',') if keyword.strip()]
    
    # Get related posts from the same category
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.is_approved = False  # Comments need approval by default
            comment.save()
            
            # Send notification to admins about new comment
            from apps.users.models import User
            from apps.notifications.models import Notification
            admin_users = [user for user in User.objects.filter(is_active=True) if user.is_admin]
            
            for admin in admin_users:
                Notification.objects.get_or_create(
                    user=admin,
                    title=f'New Comment on "{post.title}"',
                    message=f'A new comment by {comment.author_name} needs your approval.',
                    notification_type='info'
                )
            
            messages.success(request, 'Thank you for your comment! It will be reviewed and published soon.')
            return redirect('blog:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    # Get categories with post counts
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'post': post,
        'keywords_list': keywords_list,
        'related_posts': related_posts,
        'comments': comments,
        'categories': categories,
        'comment_form': comment_form,
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
        query_filters = [
            Q(title__icontains=query),
            Q(content__icontains=query),
            Q(excerpt__icontains=query)
        ]
        posts = Post.objects.filter(
            reduce(operator.or_, query_filters)
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

# Blog Management Views
@login_required
def post_management(request):
    """Manage blog posts"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all posts with filtering
    posts = Post.objects.select_related('author', 'category').order_by('-created_at')
    
    if search_query:
        query_filters = [
            Q(title__icontains=search_query),
            Q(content__icontains=search_query)
        ]
        posts = posts.filter(reduce(operator.or_, query_filters))
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'blog/post_management.html', context)

@login_required
def create_post(request):
    """Create a new blog post"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Auto-generate slug if not provided
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog:post_management')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'form_title': 'Create New Post',
    }
    return render(request, 'blog/post_form.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing blog post"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # Auto-generate slug if not provided
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog:post_management')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'form_title': 'Edit Post',
        'post': post,
    }
    return render(request, 'blog/post_form.html', context)

@login_required
def delete_post(request, post_id):
    """Delete a blog post"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog:post_management')
    
    context = {
        'post': post,
    }
    return render(request, 'blog/post_confirm_delete.html', context)

# Category Management Views
@login_required
def category_management(request):
    """Manage blog categories"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'blog/category_management.html', context)

@login_required
def create_category(request):
    """Create a new blog category"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Check if we should redirect back to post form
    next_url = request.GET.get('next')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            # Auto-generate slug if not provided
            if not category.slug:
                category.slug = slugify(category.name)
            category.save()
            messages.success(request, 'Blog category created successfully!')
            
            # Redirect back to post form if specified, otherwise to category management
            if next_url and 'post' in next_url:
                return redirect(next_url)
            else:
                return redirect('blog:category_management')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'form_title': 'Create New Category',
    }
    return render(request, 'blog/category_form.html', context)

@login_required
def edit_category(request, category_id):
    """Edit an existing blog category"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            # Auto-generate slug if not provided
            if not category.slug:
                category.slug = slugify(category.name)
            category.save()
            messages.success(request, 'Blog category updated successfully!')
            return redirect('blog:category_management')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'form_title': 'Edit Category',
    }
    return render(request, 'blog/category_form.html', context)

# Comment Management Views
@login_required
def comment_management(request):
    """Manage blog comments"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    # Get filters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Get all comments with filtering
    comments = Comment.objects.select_related('post').order_by('-created_at')
    
    if search_query:
        query_filters = [
            Q(author_name__icontains=search_query),
            Q(author_email__icontains=search_query),
            Q(content__icontains=search_query)
        ]
        comments = comments.filter(reduce(operator.or_, query_filters))
    
    if status_filter == 'approved':
        comments = comments.filter(is_approved=True)
    elif status_filter == 'pending':
        comments = comments.filter(is_approved=False)
    
    # Pagination
    paginator = Paginator(comments, 10)  # Show 10 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'comments': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'blog/comment_management.html', context)

@login_required
def edit_comment(request, comment_id):
    """Edit an existing blog comment"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog comment updated successfully!')
            return redirect('blog:comment_management')
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'form_title': 'Edit Comment',
    }
    return render(request, 'blog/comment_form.html', context)

@login_required
def delete_comment(request, comment_id):
    """Delete a blog comment"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Blog comment deleted successfully!')
        return redirect('blog:comment_management')
    
    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment_confirm_delete.html', context)

@login_required
def approve_comment(request, comment_id):
    """Approve a blog comment"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    
    messages.success(request, 'Blog comment approved successfully!')
    return redirect('blog:comment_management')

@login_required
def unapprove_comment(request, comment_id):
    """Unapprove a blog comment"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('core:dashboard')
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = False
    comment.save()
    
    messages.success(request, 'Blog comment unapproved successfully!')
    return redirect('blog:comment_management')