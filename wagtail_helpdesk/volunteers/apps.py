from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VolunteersConfig(AppConfig):
    name = "wagtail_helpdesk.volunteers"
    verbose_name = _("Volunteers")
