from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailHelpdeskVolunteersConfig(AppConfig):
    name = "wagtail_helpdesk.volunteers"
    label = "wagtail_helpdesk_volunteers"
    verbose_name = _("Volunteers")
