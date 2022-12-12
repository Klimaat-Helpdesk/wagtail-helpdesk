from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail_helpdesk.core.models import Question


class TagWidget(forms.CheckboxSelectMultiple):
    option_template_name = "core/forms/tag_option.html"


class QuestionForm(forms.ModelForm):
    """
    Form used when users ask a new question. Fields are combined into
    one field for the GitLab integration.
    """

    categories = forms.MultipleChoiceField(widget=TagWidget, choices=[], required=False)
    question = forms.CharField(max_length=1000, required=True, label="Mijn vraag is*")
    relevant_location = forms.CharField(
        max_length=1000,
        required=False,
        label="Locatie (bijvoorbeeld Amsterdam of Europa)",
    )
    relevant_timespan = forms.CharField(
        max_length=1000,
        required=False,
        label="Tijdperk (bijvoorbeeld de komende 10 jaar)",
    )
    extra_info = forms.CharField(
        max_length=5000, required=False, label="Aanvullende informatie"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from wagtail_helpdesk.cms.models import AnswerCategory  # noqa

        self.fields["categories"].choices = [
            (c.name, c.name) for c in AnswerCategory.objects.all()
        ]

    class Meta:
        model = Question
        fields = [
            "categories",
            "question",
            "relevant_location",
            "relevant_timespan",
            "extra_info",
        ]


class KeepMePostedForm(forms.ModelForm):
    """
    Form used to allow users to give their email address, this will
    update the question they asked before. Not a required step.
    """

    user_email = forms.EmailField(required=False)
    accept_terms = forms.BooleanField(
        label=_("Ik heb de algemene voorwaarden gelezen en ga er mee akkoord"),
        required=True,
    )

    class Meta:
        model = Question
        fields = [
            "user_email",
            "accept_terms",
        ]
