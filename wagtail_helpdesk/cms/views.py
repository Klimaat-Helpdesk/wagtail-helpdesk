from django.conf import settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from wagtail_helpdesk.cms.models import AnswerIndexPage


@xframe_options_exempt
def iframe_search_widget(request):
    return render(
        request,
        "cms/iframe_search_widget.html",
        {
            "title": request.GET.get("title", "Zoeken"),
            "answers_page": f"{settings.BASE_URL}{AnswerIndexPage.objects.first().url}",
        },
    )
