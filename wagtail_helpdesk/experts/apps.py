from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailHelpdeskExpertsConfig(AppConfig):
    name = "wagtail_helpdesk.experts"
    label = "wagtail_helpdesk_experts"
    verbose_name = _("Experts")
