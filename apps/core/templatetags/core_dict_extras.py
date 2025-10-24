from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a variable key"""
    return dictionary.get(key)

@register.filter
def attr(obj, attr_name):
    """Get an attribute from an object"""
    return getattr(obj, attr_name, None)