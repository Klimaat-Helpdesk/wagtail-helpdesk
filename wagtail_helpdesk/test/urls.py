from django.contrib import admin
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail_helpdesk.core.urls import urlpatterns as core_urlpatterns
from wagtail_helpdesk.experts.urls import urlpatterns as experts_urlpatterns
from wagtail_helpdesk.users.urls import urlpatterns as users_urlpatterns

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(core_urlpatterns)),
    path("", include(experts_urlpatterns)),
    path("", include(users_urlpatterns)),
    path("", include(wagtail_urls)),
]
