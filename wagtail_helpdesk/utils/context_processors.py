from django.conf import settings

from wagtail_helpdesk.cms.models import HomePage


def settings_context(_request):
    return {"settings": settings}


def defaults(request):
    home_page = HomePage.objects.first()
    if home_page:
        menu_qs = home_page.get_children().live().in_menu()
    else:
        menu_qs = None

    return {"main_nav": menu_qs}
