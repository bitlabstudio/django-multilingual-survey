"""Tests for the models of the multilingual_survey app."""
from django.test import TestCase

from . import factories


class SurveyTestCase(TestCase):
    """Tests for the ``Survey`` model."""
    def test_model(self):
        obj = factories.SurveyFactory()
        self.assertTrue(obj.pk)
