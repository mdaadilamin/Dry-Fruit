from apps.cms.models import FooterContent, ContactInfo

def footer_content(request):
    """Context processor to add footer content to all templates"""
    try:
        footer = FooterContent.objects.get(is_active=True)
    except FooterContent.DoesNotExist:
        footer = None
    
    return {
        'footer_content': footer
    }

def contact_info(request):
    """Context processor to add contact information to all templates"""
    try:
        contact = ContactInfo.objects.get(id=1)
    except ContactInfo.DoesNotExist:
        contact = None
    
    return {
        'contact_info': contact
    }