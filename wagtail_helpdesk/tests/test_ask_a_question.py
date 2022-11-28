import pytest
from django.urls import reverse

from wagtail_helpdesk.core.models import Question
from wagtail_helpdesk.tests.factories import AnswerCategoryFactory, AnswerFactory

pytestmark = pytest.mark.django_db


def test_ask_a_question(django_app):
    category = AnswerCategoryFactory(name="My category")
    AnswerFactory(categories=[category], type="answer")

    assert Question.objects.exists() is False

    response = django_app.get("/ask")
    form = response.form

    form["categories"] = [category.name]
    form["main_question"] = "This is my main question"
    form["relevant_location"] = "Here's some relevant information"
    form["relevant_timespan"] = "Have a relevant timespan as well"
    form["extra_info"] = "Let's finish with some extra info"

    result = form.submit()
    assert result.url == reverse("post-question")
    question = Question.objects.get()
    assert question.categories == "['My category']"
    assert question.question == "This is my main question"
    assert question.relevant_location == "Here's some relevant information"
    assert question.relevant_timespan == "Have a relevant timespan as well"
    assert question.extra_info == "Let's finish with some extra info"
