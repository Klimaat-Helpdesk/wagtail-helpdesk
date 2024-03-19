from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt

from wagtail_helpdesk.cms.models import AnswerIndexPage


@xframe_options_exempt
def iframe_search_widget(request):
    return render(
        request,
        "wagtail_helpdesk/cms/iframe_search_widget.html",
        {
            "title": request.GET.get("title", _("Search")),
            "answers_page": f"{settings.WAGTAILADMIN_BASE_URL}{AnswerIndexPage.objects.first().url}",
            "base_url": settings.WAGTAILADMIN_BASE_URL,
        },
    )
