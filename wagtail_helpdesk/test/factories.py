from factory import Faker
from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory

from wagtail_helpdesk.cms.models import (
    Answer,
    AnswerCategory,
    AnswerIndexPage,
    ExpertIndexPage,
)
from wagtail_helpdesk.experts.models import Expert


class AnswerCategoryFactory(DjangoModelFactory):
    name = Faker("word")
    slug = Faker("slug")
    description = Faker("sentence")

    class Meta:
        model = AnswerCategory
        django_get_or_create = ["slug"]


class AnswerFactory(PageFactory):
    content = Faker("paragraph")
    excerpt = Faker("sentence")

    class Meta:
        model = Answer


class ExpertFactory(DjangoModelFactory):
    name = Faker("name")
    bio = Faker("sentence")
    affiliation = Faker("word")

    class Meta:
        model = Expert


class ExpertIndexPageFactory(PageFactory):
    subtitle = Faker("sentence")

    class Meta:
        model = ExpertIndexPage


class AnswerIndexPageFactory(PageFactory):
    class Meta:
        model = AnswerIndexPage
