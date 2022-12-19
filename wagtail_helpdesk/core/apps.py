from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailHelpdeskCoreConfig(AppConfig):
    name = "wagtail_helpdesk.core"
    label = "wagtail_helpdesk_core"
    verbose_name = _("Core App")
