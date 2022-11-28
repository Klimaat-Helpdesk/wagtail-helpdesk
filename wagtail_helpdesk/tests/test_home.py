import pytest

from wagtail_helpdesk.tests.factories import (
    AnswerCategoryFactory,
    AnswerFactory,
    AnswerIndexPageFactory,
    ExpertFactory,
    ExpertIndexPageFactory,
)

pytestmark = pytest.mark.django_db


def test_homepage_context(django_app):
    featured_answers = AnswerFactory.create_batch(size=2, featured=True)
    not_featured_answer = AnswerFactory(featured=False)

    answer_categories = AnswerCategoryFactory.create_batch(size=2)
    featured_experts = ExpertFactory.create_batch(size=2, featured=True)
    not_featured_expert = ExpertFactory(featured=False)
    answer_index_page = AnswerIndexPageFactory(slug="answers")
    expert_index_page = ExpertIndexPageFactory(slug="experts")

    response = django_app.get("/")
    context = response.context

    assert context["answers_page"] == answer_index_page.url
    assert context["experts_page"] == expert_index_page

    assert len(context["featured_answers"]) == 2
    for featured_answer in featured_answers:
        assert featured_answer in context["featured_answers"]
    assert not_featured_answer not in context["featured_answers"]

    assert len(context["categories"]) == 2
    for category in answer_categories:
        assert category in context["categories"]

    assert len(context["featured_experts"]) == 2
    for expert in featured_experts:
        assert expert in context["featured_experts"]
    assert not_featured_expert not in context["featured_experts"]
