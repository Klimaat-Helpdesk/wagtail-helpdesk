from http import HTTPStatus

import pytest
from django.urls import reverse

from wagtail_helpdesk.tests.factories import AnswerFactory, ExpertFactory

pytestmark = pytest.mark.django_db


def test_expert_answer_overview_page(django_app):
    expert, other_expert = ExpertFactory.create_batch(size=2)
    answer = AnswerFactory(experts=[expert])
    shared_answer = AnswerFactory(experts=[expert, other_expert])
    other_answer = AnswerFactory(experts=[other_expert])

    response = django_app.get(reverse("expert_answer_overview", args=(expert.pk,)))
    context = response.context
    assert answer in context["answers"]
    assert shared_answer in context["answers"]
    assert other_answer not in context["answers"]
    assert context["expert"] == expert


def test_expert_answer_overview_page_expert_not_found(django_app):
    response = django_app.get(
        reverse("expert_answer_overview", args=(99999,)), expect_errors=True
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
