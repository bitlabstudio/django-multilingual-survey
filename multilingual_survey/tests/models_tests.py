"""Tests for the models of the multilingual_survey app."""
from django.test import TestCase

from . import factories


class SurveyTestCase(TestCase):
    """Tests for the ``Survey`` model."""
    longMessage = True

    def test_model(self):
        obj = factories.SurveyFactory()
        self.assertTrue(obj.pk)


class SurveyQuestionTestCase(TestCase):
    """Tests for the ``SurveyQuestion`` model."""
    longMessage = True

    def test_model(self):
        obj = factories.SurveyQuestionFactory()
        self.assertTrue(obj.pk)


class SurveyAnswerTestCase(TestCase):
    """Tests for the ``SurveyAnswer`` model."""
    longMessage = True

    def test_model(self):
        obj = factories.SurveyAnswerFactory()
        self.assertTrue(obj.pk)


class SurveyResponseTestCase(TestCase):
    """Tests for the ``SurveyResponse`` model."""
    longMessage = True

    def test_model(self):
        obj = factories.SurveyResponseFactory()
        self.assertTrue(obj.pk)
