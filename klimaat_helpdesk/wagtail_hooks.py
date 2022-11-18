from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from wagtail.core import hooks


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        path('jsi18n/', JavaScriptCatalog.as_view(packages=['klimaat_helpdesk']), name='javascript_catalog'),

        # Add your other URLs here, and they will appear under `/admin/klimaat_helpdesk/`
        # Note: you do not need to check for authentication in views added here, Wagtail does this for you!
    ]

    return [
        path(
            "klimaat_helpdesk/",
            include(
                (urls, "klimaat_helpdesk"),
                namespace="klimaat_helpdesk",
            ),
        )
    ]
