from django import template 

register = template.Library()

@register.filter


def ensure_scheme(url):
    """
    Ensure the given URL has a scheme (http:// or https://). If not, prepend https://.
    """
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url