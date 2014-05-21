"""Models for the multilingual_survey app"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields


class Survey(TranslatableModel):
    """
    A Survey consists of several Questions.

    :title: The name of this survey. Authors may change the name.
    :slug: The slug of this survey. The slug should never be changed, since it
      might be referenced in the code.

    """
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Name'), max_length=256)
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=256,
    )
