from django.urls import include, path

from wagtail_helpdesk.users.urls import urlpatterns as users_urlpatterns
from wagtail_helpdesk.cms.urls import urlpatterns as cms_urlpatterns

# Provide a single urls file for the whole project to make integration easier
urlpatterns = [
    path("", include(users_urlpatterns)),
    path("", include(cms_urlpatterns)),
]
