"""Tests for the forms of the multilingual_survey app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .. import forms
from . import factories


class SurveyFormTestCase(TestCase):
    """Tests for the ``SurveyForm``."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer1 = factories.SurveyAnswerFactory()
        self.question1 = self.answer1.question
        self.survey = self.question1.survey
        self.answer2 = factories.SurveyAnswerFactory()

    def test_form(self):
        form = forms.SurveyForm(self.user, self.survey, data={})
        self.assertTrue(form.is_valid(), msg=(
            'Should be valid. Errors: {0}'.format(form.errors.items())))
