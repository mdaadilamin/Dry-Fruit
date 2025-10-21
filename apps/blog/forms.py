from django import forms
from django.utils.text import slugify
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'category', 'excerpt', 'content',
            'featured_image', 'is_featured', 'status',
            'meta_title', 'meta_description', 'keywords'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category queryset only active categories
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Add help text for status field
        self.fields['status'].help_text = "Select 'Published' to make the post visible on the website"
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        title = self.cleaned_data.get('title')
        
        # If no slug provided, generate from title
        if not slug and title:
            slug = slugify(title)
        
        # Check if slug is unique (excluding current instance if editing)
        queryset = Post.objects.filter(slug=slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("This slug is already in use. Please choose a different one or modify the existing slug.")
        
        return slug
    
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if meta_title and len(meta_title) > 200:
            raise forms.ValidationError("Meta title cannot exceed 200 characters.")
        return meta_title
    
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError("Meta description cannot exceed 160 characters.")
        return meta_description
    
    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords')
        if keywords:
            # Split by comma and clean up
            keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            if len(keyword_list) > 20:  # Limit to 20 keywords
                raise forms.ValidationError("You can only specify up to 20 keywords.")
        return keywords

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        # Check if name is unique (excluding current instance if editing)
        queryset = Category.objects.filter(name=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("A category with this name already exists.")
        
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        name = self.cleaned_data.get('name')
        
        # If no slug provided, generate from name
        if not slug and name:
            slug = slugify(name)
        
        # Check if slug is unique (excluding current instance if editing)
        queryset = Category.objects.filter(slug=slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("This slug is already in use. Please choose a different one.")
        
        return slug