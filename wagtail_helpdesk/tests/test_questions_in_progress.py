import pytest

from wagtail_helpdesk.core.models import Question
from wagtail_helpdesk.tests.factories import (
    AnswerIndexPageFactory,
    ExpertFactory,
    ExpertIndexPageFactory,
    QuestionFactory,
)

pytestmark = pytest.mark.django_db


def test_questions_in_progress_context(home_page, django_app):
    featured_experts = ExpertFactory.create_batch(size=2, featured=True)
    not_featured_expert = ExpertFactory(featured=False)
    approved_questions = QuestionFactory.create_batch(size=2, status=Question.APPROVED)
    not_approved_question = QuestionFactory(status=Question.UNDECIDED)

    answer_index_page = AnswerIndexPageFactory(parent=home_page, slug="answers")
    expert_index_page = ExpertIndexPageFactory(parent=home_page, slug="experts")

    response = django_app.get("/in_behandeling")
    context = response.context

    assert context["answers_page"] == answer_index_page.url
    assert context["experts_page"] == expert_index_page

    assert len(context["featured_experts"]) == 2
    for expert in featured_experts:
        assert expert in context["featured_experts"]
    assert not_featured_expert not in context["featured_experts"]

    assert len(context["questions_in_progress"]) == 2
    for question in approved_questions:
        assert question in context["questions_in_progress"]
    assert not_approved_question not in context["questions_in_progress"]
