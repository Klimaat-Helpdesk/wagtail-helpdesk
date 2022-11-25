from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsConfig(AppConfig):
    name = "wagtail_helpdesk.cms"
    verbose_name = _("Q&A CMS")

    def ready(self):
        # Fix partial matching
        # https://github.com/wagtail/wagtail/issues/7720
        from wagtail.search.backends.database.postgres.postgres import (
            PostgresSearchQueryCompiler,
        )

        PostgresSearchQueryCompiler.LAST_TERM_IS_PREFIX = True
