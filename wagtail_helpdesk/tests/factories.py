from factory import Faker
from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory

from wagtail_helpdesk.cms.models import (
    Answer,
    AnswerCategory,
    AnswerIndexPage,
    ExpertIndexPage,
    HomePage,
    QuestionsInProgressPage,
)
from wagtail_helpdesk.core.models import Question
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


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage


class QuestionFactory(DjangoModelFactory):
    question = Faker("sentence")
    original_question = Faker("sentence")
    relevant_timespan = Faker("sentence")
    relevant_location = Faker("sentence")
    extra_info = Faker("sentence")
    categories = Faker("sentence")
    user_email = Faker("email")
    asked_by_ip = Faker("ipv4")

    class Meta:
        model = Question


class QuestionsInProgressPageFactory(PageFactory):
    class Meta:
        model = QuestionsInProgressPage
