import pytest
from wagtail.core.models import Site

from wagtail_helpdesk.tests.factories import HomePageFactory


@pytest.fixture()
def home_page():
    site = Site.objects.get()
    home_page = HomePageFactory()
    site.root_page = home_page
    site.save()
    return home_page
