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

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
    )
