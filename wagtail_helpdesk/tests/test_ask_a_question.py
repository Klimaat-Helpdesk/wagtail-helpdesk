import pytest

from wagtail_helpdesk.core.models import Question
from wagtail_helpdesk.tests.factories import (
    AnswerCategoryFactory,
    AnswerFactory,
    AskQuestionPageFactory,
)

pytestmark = pytest.mark.django_db


def test_ask_a_question(django_app, home_page):
    category = AnswerCategoryFactory(name="My category")
    AnswerFactory(categories=[category], type="answer")

    assert Question.objects.exists() is False

    ask_a_question_page = AskQuestionPageFactory(
        parent=home_page, slug="ask-a-question"
    )
    response = django_app.get(ask_a_question_page.url)
    form = response.form

    form["categories"] = [category.name]
    form["question"] = "This is my question"
    form["relevant_location"] = "Here's some relevant information"
    form["relevant_timespan"] = "Have a relevant timespan as well"
    form["extra_info"] = "Let's finish with some extra info"

    result = form.submit()
    assert result.url == ask_a_question_page.reverse_subpage("keep-me-posted")
    question = Question.objects.get()
    assert question.categories == "['My category']"
    assert question.question == "This is my question"
    assert question.relevant_location == "Here's some relevant information"
    assert question.relevant_timespan == "Have a relevant timespan as well"
    assert question.extra_info == "Let's finish with some extra info"

    keep_me_posted_form = result.follow().form
    keep_me_posted_form["user_email"] = "my@emailaddress.com"
    keep_me_posted_form["accept_terms"] = True

    result = keep_me_posted_form.submit()
    assert result.url == ask_a_question_page.url + ask_a_question_page.reverse_subpage(
        "thank-you"
    )

    question.refresh_from_db()
    assert question.user_email == "my@emailaddress.com"
