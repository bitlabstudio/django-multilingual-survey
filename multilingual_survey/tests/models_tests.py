"""Tests for the models of the multilingual_survey app."""
from django.test import TestCase

from mixer.backend.django import mixer


class SurveyTestCase(TestCase):
    """Tests for the ``Survey`` model."""
    longMessage = True

    def test_model(self):
        obj = mixer.blend('multilingual_survey.SurveyTranslation')
        self.assertTrue(obj.pk)


class SurveyQuestionTestCase(TestCase):
    """Tests for the ``SurveyQuestion`` model."""
    longMessage = True

    def test_model(self):
        obj = mixer.blend('multilingual_survey.SurveyQuestionTranslation')
        self.assertTrue(obj.pk)


class SurveyAnswerTestCase(TestCase):
    """Tests for the ``SurveyAnswer`` model."""
    longMessage = True

    def test_model(self):
        obj = mixer.blend('multilingual_survey.SurveyAnswerTranslation')
        self.assertTrue(obj.pk)


class SurveyResponseTestCase(TestCase):
    """Tests for the ``SurveyResponse`` model."""
    longMessage = True

    def test_model(self):
        obj = mixer.blend('multilingual_survey.SurveyResponse')
        self.assertTrue(obj.pk)
