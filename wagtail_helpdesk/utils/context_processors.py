from django.conf import settings

from wagtail_helpdesk.cms.models import AnswerIndexPage, HomePage


def settings_context(_request):
    return {"settings": settings}


def defaults(request):
    home_page = HomePage.objects.first()
    if home_page:
        menu_qs = home_page.get_children().live().in_menu()
    else:
        menu_qs = None
    answer_index_page = AnswerIndexPage.objects.first()
    return {
        "main_nav": menu_qs,
        "answers_list_url": answer_index_page.url if answer_index_page else "",
    }
