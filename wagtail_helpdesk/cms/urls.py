from django.urls import path

from wagtail_helpdesk.cms.views import iframe_search_widget

app_name = "cms"

urlpatterns = [
    path(
        "iframe-search-widget", view=iframe_search_widget, name="iframe-search-widget"
    ),
]
