"""Models for the multilingual_survey app"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields


class Survey(TranslatableModel):
    """
    A Survey consists of several Questions.

    :title: The name of this survey. Authors may change the title.
    :slug: The slug of this survey. The slug should never be changed, since it
      might be referenced in the code.

    """
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Title'), max_length=256)
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=256,
    )


class SurveyQuestion(TranslatableModel):
    """
    Belongs to a Survey and has several SurveyAnswers.

    :title: The title of this question.
    :content: An optional longer description of this question.
    :survey: FK to Survey.
    :is_multi_select: If ``True``, we will render checkboxes instead of
      radiobuttons or a drop-down-list..
    :position: Can be used to order questions in a survey.

    """
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Title'), max_length=256),
        content=models.TextField(verbose_name=_('Content'))
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name=_('Survey'),
        related_name='questions',
    )

    is_multi_select = models.BooleanField(
        verbose_name=_('Is multi-select'),
        default=False,
    )

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
    )


class SurveyAnswer(TranslatableModel):
    """
    Belongs to a SurveyQuestion.

    :title: The title of this answer. Authors may change this title.
    :slug: The slug of this answer. Should never be changed since it might be
      referenced in the code.
    :position: Can be used to order answers.

    """
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Title'), max_length=256),
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=256,
    )

    question = models.ForeignKey(
        SurveyQuestion,
        verbose_name=_('Question'),
    )

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
    )


class SurveyResponse(models.Model):
    """
    Ties a user response to an answer.

    :user: Optional FK to the User. If ``None``, we are dealing with an
      anonymous answer.
    :answer: Optional FK to a SurveyAnswer. If ``None``, then ``other_answer``
      must be given.
    :other_answer: Optional free text entered by the user if no available
      answer matches him. If ``None``, then ``answer`` must be given.
    :date_created: Creation date of this answer.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        blank=True, null=True,
    )

    answer = models.ForeignKey(
        SurveyAnswer,
        verbose_name=_('Answer'),
        blank=True, null=True,
    )

    other_answer = models.CharField(
        verbose_name=_('Other answer'),
        max_length=1024,
        blank=True,
    )

    date_created = models.DateTimeField(
        verbose_name=_('Date created'),
        auto_now_add=True,
    )
