from apps.cms.models import FooterContent

def footer_content(request):
    """Context processor to add footer content to all templates"""
    try:
        footer = FooterContent.objects.get(is_active=True)
    except FooterContent.DoesNotExist:
        footer = None
    
    return {
        'footer_content': footer
    }