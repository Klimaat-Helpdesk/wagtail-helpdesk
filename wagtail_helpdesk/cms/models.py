from django.conf import settings
from django.db import models
from django.db.models import TextField
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.search import index as search_index
from wagtail.snippets.models import register_snippet

from wagtail_helpdesk.cms.blocks import (
    AnswerImageBlock,
    AnswerOriginBlock,
    AnswerRichTextBlock,
    QuoteBlock,
    RelatedItemsBlock,
)
from wagtail_helpdesk.core.forms import KeepMePostedForm, QuestionForm
from wagtail_helpdesk.core.models import Question
from wagtail_helpdesk.experts.models import Expert
from wagtail_helpdesk.volunteers.models import Volunteer

LINK_STREAM = [
    (
        "item",
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(verbose_name="Titel")),
                ("page", blocks.PageChooserBlock(verbose_name="Pagina")),
            ]
        ),
    )
]


class HomePage(Page):
    template = "wagtail_helpdesk/cms/home_page.html"

    max_count = 1

    intro = models.TextField(blank=True)
    header_buttons = StreamField(
        LINK_STREAM, blank=True, verbose_name=_("Buttons"), use_json_field=True
    )
    recent_question_title = models.CharField(
        max_length=255, verbose_name=_("Title"), blank=True
    )
    recent_question_buttons = StreamField(
        LINK_STREAM, blank=True, verbose_name=_("Buttons"), use_json_field=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("intro"),
                FieldPanel("header_buttons"),
            ],
            heading=_("Header"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("recent_question_title"),
                FieldPanel("recent_question_buttons"),
            ],
            heading=_("Recent questions"),
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "featured_answers": Answer.objects.live()
                .filter(featured=True)
                .prefetch_related(
                    "answer_expert_relationship__expert",
                    "answer_category_relationship__category",
                )
                .order_by("-first_published_at")[:10],
                "featured_experts": Expert.objects.prefetch_related(
                    "expert_answer_relationship__answer__answer_category_relationship__category"
                )
                .select_related("picture")
                .filter(featured=True)[:3],
                "answer_index_page": AnswerIndexPage.objects.live().first(),
                "expert_answers_overview_page": ExpertAnswerOverviewPage.objects.first(),
            }
        )
        return context

    class Meta:
        verbose_name = _("Homepage")
        verbose_name_plural = _("Homepages")


class ExpertAnswerRelationship(Orderable, models.Model):
    """
    Intermediate table for holding the many-to-many relationship in case there are
    many experts working on the same answer.
    """

    answer = ParentalKey(
        "Answer", related_name="answer_expert_relationship", on_delete=models.CASCADE
    )
    expert = models.ForeignKey(
        "experts.Expert",
        related_name="expert_answer_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("expert")]


class CategoryAnswerRelationship(Orderable, models.Model):
    """
    Intermediate table for holding the many-to-many relationship between categories and answers
    """

    answer = ParentalKey(
        "Answer", related_name="answer_category_relationship", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "cms.AnswerCategory",
        related_name="category_answer_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("category")]


class AnswerTag(TaggedItemBase):
    content_object = ParentalKey(
        "Answer", related_name="tagged_items", on_delete=models.CASCADE
    )


class AnswerCategory(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(
        verbose_name=_("slug"),
        allow_unicode=True,
        max_length=50,
        help_text=_("A slug to identify the category"),
    )
    description = models.CharField(
        _("description"), max_length=255, blank=False, null=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = _("Answer Category")
        verbose_name_plural = _("Answer Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_prefiltered_search_params(self):
        return "?{}=".format(self.name)


register_snippet(AnswerCategory)


class Answer(Page):
    template = "wagtail_helpdesk/cms/answer_detail.html"

    # Determines type and whether its highlighted in overview list
    type = models.CharField(
        choices=[("answer", "Antwoord"), ("column", "Column")],
        max_length=100,
        default="answer",
        help_text=_(
            "Choose between answer or discussion piece with a more prominent look"
        ),
    )
    featured = models.BooleanField(default=False)

    content = RichTextField(blank=True)
    excerpt = models.CharField(
        verbose_name=_("Short description"),
        max_length=255,
        blank=False,
        null=True,
        help_text=_("This helps with search engines and when sharing on social media"),
    )
    introduction = TextField(
        verbose_name=_("Introduction"),
        default="",
        blank=True,
        null=True,
        help_text=_("This text is displayed above the tags, useful as a TLDR section"),
    )
    tags = ClusterTaggableManager(through=AnswerTag, blank=True)

    social_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the image that will be displayed when sharing on social media"
        ),
    )

    # Freeform content of answer
    page_content = StreamField(
        [
            ("richtext", AnswerRichTextBlock()),
            ("image", AnswerImageBlock()),
            ("quote", QuoteBlock()),
        ],
        use_json_field=True,
    )

    # Which experts and how was this answered?
    answer_origin = StreamField(
        [("origin", AnswerOriginBlock())], blank=True, use_json_field=True
    )

    # Related items
    related_items = StreamField(
        [("related_items", RelatedItemsBlock())], blank=True, use_json_field=True
    )

    parent_page_types = ["AnswerIndexPage"]

    content_panels = Page.content_panels + [
        FieldPanel("type"),
        FieldPanel("featured", heading=_("Show this answer on the home page")),
        FieldPanel(
            "excerpt",
            classname="full",
        ),
        FieldPanel("introduction", classname="full"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "answer_category_relationship",
                    label=_("Categorie(n)"),
                    panels=None,
                    min_num=1,
                )
            ],
            heading=_("Categorie(s)"),
        ),
        FieldPanel(
            "tags",
            heading="Please use tags with a maximum length of 16 characters per single word to avoid overlap in the mobile view.",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "answer_expert_relationship",
                    label=_("Expert(s)"),
                    panels=None,
                    min_num=1,
                )
            ],
            heading=_("Expert(s)"),
        ),
        FieldPanel("page_content"),
        FieldPanel("answer_origin"),
        FieldPanel("related_items"),
        FieldPanel(
            "social_image", help_text=_("Image to be used when sharing on social media")
        ),
    ]

    search_fields = Page.search_fields + [
        search_index.FilterField("type"),
        search_index.SearchField("page_content"),
    ]

    @property
    def experts(self):
        experts = [n.expert for n in self.answer_expert_relationship.all()]
        return experts

    @property
    def categories(self):
        categories = [n.category for n in self.answer_category_relationship.all()]
        return categories

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    def get_references(self):
        """
        Build reference list, in the order Wagtail returns them.  ### , alphabetically to sort of comply with standards

        TODO: References for articles can be separated from the origin and make them a proper ListBlock that can be
            handled by editors as they see fit. Having the references within a StreamField of 'origins' seems counter
            intuitive.

        """
        ref_list = []
        try:
            component = self.answer_origin[0]
        except IndexError:
            return ref_list

        # Access streamfield elements
        for element in component.value["sources"]:
            ref_list.append(
                {
                    "text": element["reference_text"],
                    "url": element["url_or_doi"],
                }
            )

        # Sort by text starting letter, best we can do for now
        # ref_list.sort(key=lambda e: e['text'])
        return ref_list

    def get_primary_expert(self):
        """
        Gets the first expert associated with this answer if it exists.
        """
        try:
            first = self.experts[0]
        except IndexError:
            return _("Unknown")
        else:
            return first

    def get_all_categories(self):
        return [
            {"title": c.name, "url": c.get_prefiltered_search_params()}
            for c in self.categories
        ]

    def get_card_data(self):
        return {
            "title": self.title,
            "url": self.url,
            "author": self.get_primary_expert(),
            "categories": self.get_all_categories(),
            "type": "answer",
        }

    def get_as_overview_row_card(self):
        if self.type == "answer":
            return render_to_string(
                "wagtail_helpdesk/core/includes/answer_block.html",
                context=self.get_card_data(),
            )
        else:  # It's a column
            return render_to_string(
                "wagtail_helpdesk/core/includes/column_block.html",
                context=self.get_card_data(),
            )

    def get_as_home_row_card(self):
        return render_to_string(
            "wagtail_helpdesk/core/includes/answer_home_block.html",
            context=self.get_card_data(),
        )

    def get_as_related_row_card(self):
        return render_to_string(
            "wagtail_helpdesk/core/includes/related_item_block.html",
            context=self.get_card_data(),
        )

    def get_context(self, request, *args, **kwargs):
        context = super(Answer, self).get_context(request, *args, **kwargs)

        categories = AnswerCategory.objects.all()

        context.update(
            {
                "categories": categories,
                "answers_page": AnswerIndexPage.objects.first().url,
                "experts_page": ExpertIndexPage.objects.first(),
            }
        )
        return context

    class Meta:
        ordering = [
            "-first_published_at",
        ]


class AnswerIndexPage(RoutablePageMixin, Page):
    """List of answers on the website"""

    template = "wagtail_helpdesk/cms/answers_list.html"

    subpage_types = ["Answer"]

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerIndexPage, self).get_context(request, *args, **kwargs)

        answers = (
            Answer.objects.descendant_of(self)
            .live()
            .filter(type="answer")
            .specific()
            .order_by("-first_published_at")
        )
        columns = (
            Answer.objects.live()
            .filter(type="column")
            .specific()
            .order_by("-first_published_at")
        )

        # Search
        search = request.GET.get("search", "")
        context["search"] = search
        if search:
            answers = answers.search(search).get_queryset()
            columns = columns.search(search).get_queryset()

        # Filter categories based on GET params
        chosen_categories = []
        for filter in request.GET:
            try:
                category = AnswerCategory.objects.get(name__iexact=filter)
            except AnswerCategory.DoesNotExist:
                # In case someone puts weird stuff in the url
                pass
            else:
                chosen_categories.append(category)

        if len(chosen_categories) > 0:
            answers = answers.filter(
                answer_category_relationship__category__in=chosen_categories
            )
            columns = columns.filter(
                answer_category_relationship__category__in=chosen_categories
            )

        # Adjust categories to maintain checked status
        categories = AnswerCategory.objects.all()
        categories_context = [
            {"category": c, "selected": True if c in chosen_categories else False}
            for c in categories
        ]

        # Insert column every 3 answers
        answers_and_columns = list(answers)
        if len(columns) > 0:
            # INTERSPACING = len(answers) // len(columns) # Can be used to spread evenly if desired
            INTERSPACING = 3
            if len(answers) >= INTERSPACING:
                column_index = 0
                for index in range(len(answers)):
                    if index != 0 and index % INTERSPACING == 0:
                        try:
                            answers_and_columns.insert(
                                index + column_index, columns[column_index]
                            )
                        except IndexError:
                            break
                        else:
                            column_index += 1
            # List is too short, cannot interspace, so just put them at the end
            else:
                answers_and_columns += list(columns)

        context.update(
            {
                "answers_page": AnswerIndexPage.objects.first().url,
                "categories": categories_context,
                "answers_and_columns": answers_and_columns,
                "experts_page": ExpertIndexPage.objects.first(),
            }
        )
        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = AnswerCategory.objects.get(slug=cat_slug)
        except AnswerCategory.DoesNotExist:
            return redirect("/")

        context.update(
            {
                "answers": Answer.objects.live().public().filter(category=category),
                "subtitle": category.description,
            }
        )

        return render(request, self.template, context)


class ExpertIndexPage(Page):
    """List of experts on the website"""

    template = "wagtail_helpdesk/experts/experts_list.html"

    subtitle = models.CharField(max_length=128, blank=False)
    intro = RichTextField(blank=True)
    outro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("intro"),
        FieldPanel("outro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ExpertIndexPage, self).get_context(request, *args, **kwargs)
        experts = Expert.objects.all()
        categories = AnswerCategory.objects.all()

        context.update(
            {
                "experts": experts,
                "answers_page": AnswerIndexPage.objects.first().url,
                "categories": categories,
            }
        )
        return context


class ExpertAnswerOverviewPage(RoutablePageMixin, Page):
    template = "wagtail_helpdesk/cms/expert_answer_overview_page.html"

    preview_modes = []
    max_count = 1

    @route(r"^$")
    def index(self, request, *args, **kwargs):
        """This page does not exist. It's only used for expert_answers"""
        raise Http404

    @route(r"^(\d+)/$")
    def expert_answers(self, request, expert_id):
        expert = get_object_or_404(Expert, pk=expert_id)
        answers = expert.get_answered_questions()

        return self.render(
            request, context_overrides={"expert": expert, "answers": answers}
        )


class VolunteerIndexPage(Page):
    """List of volunteers on the website"""

    template = "wagtail_helpdesk/volunteers/volunteers_list.html"

    subtitle = models.CharField(max_length=128, blank=False)
    intro = RichTextField(blank=True)
    outro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("intro"),
        FieldPanel("outro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(VolunteerIndexPage, self).get_context(request, *args, **kwargs)
        volunteers = Volunteer.objects.all()

        context.update(
            {
                "volunteers": volunteers,
                "answers_page": AnswerIndexPage.objects.first().url,
            }
        )
        return context


class GeneralPage(Page):
    """A page that won't show sidebar. Ideal for privacy policy, etc."""

    template = "wagtail_helpdesk/cms/general_page.html"

    subtitle = models.CharField(max_length=128, blank=True)

    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content"),
    ]


class QuestionsInProgressPage(Page):
    template = "wagtail_helpdesk/cms/questions_in_progress.html"

    def get_context(self, request, *args, **kwargs):
        featured_experts = Expert.objects.filter(featured=True)[:3]
        questions = Question.objects.filter(status=Question.APPROVED)
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "answers_page": AnswerIndexPage.objects.first().url,
                "experts_page": ExpertIndexPage.objects.first(),
                "featured_experts": featured_experts,
                "questions_in_progress": questions,
            }
        )
        return context

    class Meta:
        verbose_name = _("Questions in progress page")
        verbose_name_plural = _("Questions in progress pages")


class AskQuestionPage(RoutablePageMixin, Page):
    intro = RichTextField(
        verbose_name="Intro",
        default="<p>Wij willen je vraag graag zo compleet en correct mogelijk beantwoorden. "
        "Daarom vragen wij twee experts die voor jou aan de slag gaan om een antwoord te formuleren. "
        "De één doorzoekt bronnen en discussiëert, de ander gaat alles nog eens grondig controleren. "
        "Het kost wel wat tijd om deze wetenschappelijke standaard voor een betrouwbaar antwoord te behalen. "
        "Daarom kan het wat langer duren voordat je vraag beantwoord is.</p>",
    )
    step_1_title = models.CharField(
        verbose_name="Titel", max_length=255, default="Waar gaat je vraag over?"
    )
    step_2_title = models.CharField(
        verbose_name="Titel", max_length=255, default="Formuleer je vraag"
    )
    keep_me_posted_title = models.CharField(
        verbose_name="Titel", max_length=255, default="Bedankt voor je vraag!"
    )
    keep_me_posted_text = RichTextField(
        verbose_name="Tekst",
        default="<p>Laat je mailadres achter als je op de hoogte gehouden wilt worden. Dit is optioneel.</p>",
    )
    thank_you_text = RichTextField(
        verbose_name="Tekst",
        default="<p>Bedankt voor het stellen van je vraag. "
        "We nemen je vraag in behandeling en proberen zo snel mogelijk een "
        "expert te vinden die je vraag kan beantwoorden.</p>",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("intro"),
                FieldPanel("step_1_title"),
                FieldPanel("step_2_title"),
            ],
            heading="Twee-traps-formulier",
        ),
        MultiFieldPanel(
            [
                FieldPanel("keep_me_posted_title"),
                FieldPanel("keep_me_posted_text"),
            ],
            heading="Houd me op de hoogte",
        ),
        MultiFieldPanel(
            [
                FieldPanel("thank_you_text"),
            ],
            heading="Dank u!",
        ),
    ]

    @route(r"^$")
    def index(self, request, *args, **kwargs):
        """
        Index page, the form is spread over two steps using JavaScript.
        """
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.asked_by_ip = request.META.get("REMOTE_ADDR", "")
                obj.save()
                request.session["question_id"] = obj.pk
                return HttpResponseRedirect(self.reverse_subpage("keep-me-posted"))
        else:
            form = QuestionForm()

        template = "wagtail_helpdesk/cms/ask_question_page.html"
        context = self.get_context(request)
        context.update({"form": form})
        return render(request, template, context)

    @route(r"^houd-me-op-de-hoogte/$", name="keep-me-posted")
    def keep_me_posted(self, request):
        """
        Keep me posted, optional step to leave your e-mail.
        """
        question = get_object_or_404(Question, pk=request.session.get("question_id"))
        if request.method == "POST":
            form = KeepMePostedForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                del request.session["question_id"]
                return HttpResponseRedirect(
                    self.url + self.reverse_subpage("thank-you")
                )
        else:
            form = KeepMePostedForm(instance=question)

        template = "wagtail_helpdesk/cms/ask_question_page_keep_me_posted.html"
        context = self.get_context(request)
        context.update({"form": form})
        return render(request, template, context)

    @route(r"^dank/$", name="thank-you")
    def thank_you(self, request):
        template = "wagtail_helpdesk/cms/ask_question_page_thank_you.html"
        context = self.get_context(request)
        return render(request, template, context)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context.update(
            {
                "answer_index_page": AnswerIndexPage.objects.live().first(),
            }
        )
        return context


@register_setting
class MainNavSettings(BaseSetting):
    text = models.CharField(
        verbose_name=_("Text"),
        max_length=255,
        default=_("Didn't find the answer you were looking for?"),
    )
    buttons = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(verbose_name=_("Title"))),
                        ("page", blocks.PageChooserBlock(verbose_name=_("Page"))),
                    ]
                ),
            )
        ],
        verbose_name=_("Buttons"),
        blank=True,
        use_json_field=True,
    )

    class Meta:
        verbose_name = _("Main navigation")


@register_setting
class FooterSettings(BaseSetting):
    about_title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True)
    about_text = RichTextField(verbose_name=_("Text"), blank=True)
    about_buttons = StreamField(
        LINK_STREAM, blank=True, verbose_name=_("Buttons"), use_json_field=True
    )

    expert_title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True)
    expert_text = RichTextField(
        verbose_name=_("Text"),
        blank=True,
    )
    expert_buttons = StreamField(
        LINK_STREAM, blank=True, verbose_name=_("Buttons"), use_json_field=True
    )

    initiator_text = RichTextField(
        verbose_name=_("Initiator-text"),
        default='<p>An initiative of <a href="#">...</a> & <a href="#">...</a></p>',
    )
    nav = StreamField(
        LINK_STREAM, verbose_name=_("Navigation"), blank=True, use_json_field=True
    )
    maintainer_text = models.TextField(
        verbose_name=_("Maintainer text"),
        max_length=255,
        default="example.com is managed by ..., a non-profit organization, "
        "registered under Chamber of Commerce number ...",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_text"),
                FieldPanel("about_buttons"),
            ],
            heading=_("About us"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("expert_title"),
                FieldPanel("expert_text"),
                FieldPanel("expert_buttons"),
            ],
            heading=_("Experts"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("initiator_text"),
                FieldPanel("nav"),
                FieldPanel("maintainer_text"),
            ],
            heading=_("Primary footer"),
        ),
    ]

    class Meta:
        verbose_name = "Footer"


@register_setting
class StickySettings(BaseSetting):
    text = models.CharField(
        max_length=255,
        verbose_name=_("Text"),
        default=_(
            "Didn't find the answer you were looking for? Check out the pending questions or ask your own question!"
        ),
    )
    buttons = StreamField(
        LINK_STREAM, verbose_name=_("Buttons"), blank=True, use_json_field=True
    )

    class Meta:
        verbose_name = _("Sticky menu")


class SearchWidgetPage(Page):
    template = "wagtail_helpdesk/cms/search_widget_page.html"

    intro = models.TextField(
        default=_("Create a search widget to place on your own website")
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "base_url": settings.BASE_URL,
            }
        )
        return context


@register_setting
class HelpdeskSiteSettings(BaseSetting):
    site_name = models.CharField(
        verbose_name=_("Site name"), max_length=255, blank=True
    )


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter_handle = models.CharField(
        verbose_name=_("Twitter handle"), max_length=15, blank=True
    )
    short_site_name = models.CharField(
        verbose_name=_("Short site name"), max_length=255, blank=True
    )
    short_site_description = models.CharField(
        verbose_name=_("Short site description"), max_length=255, blank=True
    )
