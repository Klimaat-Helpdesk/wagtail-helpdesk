import factory
from factory import Faker
from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory

from wagtail_helpdesk.cms.models import (
    Answer,
    AnswerCategory,
    AnswerIndexPage,
    AskQuestionPage,
    CategoryAnswerRelationship,
    ExpertAnswerOverviewPage,
    ExpertAnswerRelationship,
    ExpertIndexPage,
    HomePage,
    QuestionsInProgressPage,
)
from wagtail_helpdesk.core.models import Question
from wagtail_helpdesk.experts.models import Expert


class CategoryAnswerRelationshipFactory(DjangoModelFactory):
    answer = factory.SubFactory("factories.AnswerFactory")
    category = factory.SubFactory("factories.AnswerCategoryFactory")

    class Meta:
        model = CategoryAnswerRelationship


class AnswerCategoryFactory(DjangoModelFactory):
    name = Faker("word")
    slug = Faker("slug")
    description = Faker("sentence")

    class Meta:
        model = AnswerCategory
        django_get_or_create = ["slug"]


class ExpertAnswerRelationshipFactory(DjangoModelFactory):
    answer = factory.SubFactory("factories.AnswerFactory")
    expert = factory.SubFactory("factories.ExpertFactory")

    class Meta:
        model = ExpertAnswerRelationship


class AnswerFactory(PageFactory):
    content = Faker("paragraph")
    excerpt = Faker("sentence")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if create and extracted:
            for category in extracted:
                CategoryAnswerRelationshipFactory(answer=self, category=category)

    @factory.post_generation
    def experts(self, create, extracted, **kwargs):
        if create and extracted:
            for expert in extracted:
                ExpertAnswerRelationshipFactory(answer=self, expert=expert)

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


class AskQuestionPageFactory(PageFactory):
    intro = Faker("paragraph")
    step_1_title = Faker("sentence")
    step_2_title = Faker("sentence")
    keep_me_posted_title = Faker("sentence")
    keep_me_posted_text = Faker("paragraph")
    thank_you_text = Faker("paragraph")

    class Meta:
        model = AskQuestionPage


class ExpertAnswerOverviewPageFactory(PageFactory):
    class Meta:
        model = ExpertAnswerOverviewPage
