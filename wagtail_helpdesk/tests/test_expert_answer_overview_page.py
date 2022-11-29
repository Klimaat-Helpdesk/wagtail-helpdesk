from http import HTTPStatus

import pytest

from wagtail_helpdesk.tests.factories import (
    AnswerFactory,
    ExpertAnswerOverviewPageFactory,
    ExpertFactory,
)

pytestmark = pytest.mark.django_db


def test_expert_answer_overview_page(home_page, django_app):
    expert_answer_overview_page = ExpertAnswerOverviewPageFactory(parent=home_page)
    expert, other_expert = ExpertFactory.create_batch(size=2)
    answer = AnswerFactory(experts=[expert])
    shared_answer = AnswerFactory(experts=[expert, other_expert])
    other_answer = AnswerFactory(experts=[other_expert])

    url = expert_answer_overview_page.url + expert_answer_overview_page.reverse_subpage(
        "expert_answers", args=(expert.pk,)
    )
    response = django_app.get(url)
    context = response.context
    assert answer in context["answers"]
    assert shared_answer in context["answers"]
    assert other_answer not in context["answers"]
    assert context["expert"] == expert


def test_expert_answer_overview_page_expert_not_found(home_page, django_app):
    expert_answer_overview_page = ExpertAnswerOverviewPageFactory(parent=home_page)

    response = django_app.get(expert_answer_overview_page.url, expect_errors=True)
    assert response.status_code == HTTPStatus.NOT_FOUND

    url = expert_answer_overview_page.url + expert_answer_overview_page.reverse_subpage(
        "expert_answers", args=(999999,)
    )
    response = django_app.get(url, expect_errors=True)
    assert response.status_code == HTTPStatus.NOT_FOUND
