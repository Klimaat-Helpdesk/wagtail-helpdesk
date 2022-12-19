from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Question(models.Model):
    """Main element to drive the flow of the website. Questions are what the user can ask and which will trigger the
    rest of the actions on the website
    """

    UNDECIDED = 0
    APPROVED = 1
    ANSWERED = 2
    REJECTED = 3

    STATUS_CHOICES = (
        (UNDECIDED, _("Undecided")),
        (APPROVED, _("Approved")),
        (ANSWERED, _("Answered")),
        (REJECTED, _("Rejected")),
    )

    question = models.TextField(
        verbose_name=_("Your Question"),
        help_text=_(
            "How the question is displayed on the (questions pending) page, only approved questions are shown"
        ),
        blank=False,
    )
    original_question = models.TextField(
        verbose_name=_("Original Question"), blank=True
    )
    relevant_timespan = models.TextField(
        verbose_name=_("Relevant timespan"), blank=True
    )
    relevant_location = models.TextField(
        verbose_name=_("Relevant location"), blank=True
    )
    extra_info = models.TextField(verbose_name=_("Extra information"), blank=True)
    categories = models.TextField(verbose_name=_("Categories"), blank=True)

    user_email = models.EmailField(verbose_name=_("User Email"), blank=True)
    asked_by_ip = models.GenericIPAddressField(null=True, blank=True)

    date_asked = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNDECIDED)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("question"),
                FieldPanel("status"),
            ],
            heading=_("General"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("original_question"),
                FieldPanel("relevant_timespan"),
                FieldPanel("relevant_location"),
                FieldPanel("extra_info"),
                FieldPanel("categories"),
            ],
            heading=_("Original Question"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("user_email"),
                FieldPanel("asked_by_ip"),
            ],
            heading=_("User"),
        ),
    ]

    def get_card_data(self):
        return {
            "title": self.question,
        }

    def get_as_home_row_card(self):
        return render_to_string(
            "wagtail_helpdesk/core/includes/question_list_block.html",
            context=self.get_card_data(),
        )

    def save(self, *args, **kwargs):
        if not self.original_question:
            self.original_question = self.question
        super().save(*args, **kwargs)
