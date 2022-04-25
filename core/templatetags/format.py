from django import template


register = template.Library()

@register.filter('format')
def add_format(format_str, val):
    """Checks if request url is current url"""
    return format_str.format(val)