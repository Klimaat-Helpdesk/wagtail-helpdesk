from django import template

from wagtail_helpdesk.utils.staticfiles import versioned_static as versioned_static_func

register = template.Library()


@register.simple_tag
def versioned_static(path):
    """
    Wrapper for Django's static file finder to append a cache-busting query parameter
    that updates on each Wagtail version.
    See https://github.com/wagtail/wagtail/blob/main/wagtail/admin/templatetags/wagtailadmin_tags.py#L663
    """
    return versioned_static_func(path)

#function to add a tag to the url, but replace the value if it already exists
@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    dict_ = context['request'].GET.copy()
    for k, v in kwargs.items():
        dict_[k] = v
    return dict_.urlencode()