from django.conf import settings

from wagtail_helpdesk.cms.models import HomePage


def settings_context(_request):
    return {"settings": settings}


def defaults(request):
    return {"main_nav": HomePage.objects.first().get_children().live().in_menu()}
