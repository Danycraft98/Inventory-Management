from django import template


register = template.Library()

@register.filter
def is_url(request, admin_url):
    """Checks if request url is current url"""
    full_path = request.get_full_path()
    return full_path == admin_url


@register.filter('dir')
def get_dir(val):
    return dir(val)