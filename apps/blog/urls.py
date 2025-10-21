from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search_posts'),
    
    # Blog Management URLs
    path('management/', views.post_management, name='post_management'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    
    # Category Management URLs
    path('categories/', views.category_management, name='category_management'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    
    # Comment Management URLs
    path('comments/', views.comment_management, name='comment_management'),
    path('comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comments/approve/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('comments/unapprove/<int:comment_id>/', views.unapprove_comment, name='unapprove_comment'),
]